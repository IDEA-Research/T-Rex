import argparse
import json
import random
from typing import Dict, List

import gradio as gr
import numpy as np
from gradio_image_prompter import ImagePrompter
from PIL import Image, ImageDraw, ImageFont

from trex import TRex2APIWrapper


def arg_parse():
    parser = argparse.ArgumentParser(description="Gradio Demo for T-Rex2")
    parser.add_argument(
        "--trex2_api_token",
        type=str,
        help="API token for T-Rex2",
    )
    parser.add_argument("--sam_type", type=str, default="vit_l", help="SAM model type")
    parser.add_argument(
        "--sam_checkpoint_path", type=str, help="path to checkpoint file"
    )
    args = parser.parse_args()
    return args


def plot_boxes_to_image(
    image_pil: Image,
    tgt: Dict,
    return_point: bool = False,
    point_width: float = 1.0,
    return_score=True,
) -> Image:
    """Plot bounding boxes and labels on an image.

    Args:
        image_pil (PIL.Image): The input image as a PIL Image object.
        tgt (Dict[str, Union[torch.Tensor, List[torch.Tensor]]]): The target dictionary containing
            the bounding boxes and labels. The keys are:
                - scores: A tuple containing the height and width of the image.
                - boxes: A list of normalized bounding boxes as a list of shape (N, 4), in
                    (x_center, y_center, width, height) format.
                - labels: A list of string labels for each bounding box.
        return_point (bool): Draw center point instead of bounding box. Defaults to False.

    Returns:
        Union[PIL.Image, PIL.Image]: A tuple containing the input image and ploted image.
    """
    # Get the bounding boxes and labels from the target dictionary
    boxes = tgt["boxes"]
    scores = tgt["scores"]

    # Create a PIL ImageDraw object to draw on the input image
    draw = ImageDraw.Draw(image_pil)
    # Create a new binary mask image with the same size as the input image
    mask = Image.new("L", image_pil.size, 0)
    # Create a PIL ImageDraw object to draw on the mask image
    mask_draw = ImageDraw.Draw(mask)

    # Draw boxes and masks for each box and label in the target dictionary
    for box, score in zip(boxes, scores):
        # Convert the box coordinates from 0..1 to 0..W, 0..H
        color = tuple(np.random.randint(0, 255, size=3).tolist())
        # Extract the box coordinates
        x0, y0, x1, y1 = box
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        if return_point:
            ceter_x = int((x0 + x1) / 2)
            ceter_y = int((y0 + y1) / 2)
            # Draw the center point on the input image
            draw.ellipse(
                (
                    ceter_x - point_width,
                    ceter_y - point_width,
                    ceter_x + point_width,
                    ceter_y + point_width,
                ),
                fill=color,
                width=point_width,
            )
        else:
            # Draw the box outline on the input image
            draw.rectangle([x0, y0, x1, y1], outline=color, width=int(point_width))

        # Draw the label text on the input image
        if return_score:
            text = f"{score:.2f}"
        else:
            text = f""
        font = ImageFont.load_default()
        if hasattr(font, "getbbox"):
            bbox = draw.textbbox((x0, y0), text, font)
        else:
            w, h = draw.textsize(text, font)
            bbox = (x0, y0, w + x0, y0 + h)
        if not return_point:
            draw.rectangle(bbox, fill=color)
            draw.text((x0, y0), text, fill="white")

        # Draw the box on the mask image
        mask_draw.rectangle([x0, y0, x1, y1], fill=255, width=6)
    return image_pil, mask


def multi_mask2one_mask(masks):
    _, _, h, w = masks.shape
    for i, mask in enumerate(masks):
        mask_image = mask.reshape(h, w, 1)
        whole_mask = mask_image if i == 0 else whole_mask + mask_image
    whole_mask = np.where(whole_mask == False, 0, 255)
    return whole_mask


def numpy2PIL(numpy_image):
    out = Image.fromarray(numpy_image.astype(np.uint8))
    return out


def draw_mask(mask, draw, random_color=True):
    if random_color:
        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            153,
        )
    else:
        color = (30, 144, 255, 153)

    nonzero_coords = np.transpose(np.nonzero(mask))

    for coord in nonzero_coords:
        draw.point(coord[::-1], fill=color)


def build_annotation(boxes, mask):
    annotations = []
    mask_coor = np.transpose(np.nonzero(mask)).astype(np.int32).tolist()
    for i, box in enumerate(boxes):
        # convert box from xyxy to xywh
        box = box.tolist()
        box[2] -= box[0]
        box[3] -= box[1]
        box = np.array(box).astype(np.int32).tolist()
        area = box[2] * box[3]
        annotation = {
            "id": i,
            "image_id": 0,
            "category_id": 0,
            "segmentation": [],
            "mask": mask_coor,
            "area": area,
            "bbox": box,
            "iscrowd": 0,
        }
        annotations.append(annotation)
    return json.dumps(dict(annotation=annotations))


def clean_input():
    return [None] * 9


def parse_visual_prompt(points: List):
    boxes = []
    pos_points = []
    neg_points = []
    for point in points:
        if point[2] == 2 and point[-1] == 3:
            x1, y1, _, x2, y2, _ = point
            boxes.append([x1, y1, x2, y2])
        elif point[2] == 1 and point[-1] == 4:
            x, y, _, _, _, _ = point
            pos_points.append([x, y])
        elif point[2] == 0 and point[-1] == 4:
            x, y, _, _, _, _ = point
            neg_points.append([x, y])
    return boxes, pos_points, neg_points


def pack_model_input_interactive(interactive_input):
    ref_image = interactive_input["image"]
    ref_visual_prompt = interactive_input["points"]
    boxes, pos_points, neg_points = parse_visual_prompt(ref_visual_prompt)
    # boxes and points can not show at the same time
    if len(boxes) > 0 and len(pos_points) > 0:
        raise gr.Error("You can't draw both box and point at the same time")
    if len(boxes) > 0:
        prompts = {
            "prompt_image": ref_image,
            "type": "rect",
            "prompts": [{"category_id": 1, "rects": boxes}],
        }
    else:
        prompts = {
            "prompt_image": ref_image,
            "type": "point",
            "prompts": [{"category_id": 1, "points": pos_points}],
        }
    return prompts


def pack_model_input_generic(generic_vp_dict):
    prompts = []
    for k, v in generic_vp_dict.items():
        if v is None:
            continue
        ref_image = v["image"]
        ref_visual_prompt = v["points"]
        boxes, pos_points, _ = parse_visual_prompt(ref_visual_prompt)
        # boxes and points can not show at the same time
        if len(boxes) > 0 and len(pos_points) > 0:
            raise gr.Error("You can't draw both box and point at the same time")
        if len(boxes) > 0:
            target = dict(prompt_image=ref_image, rects=boxes)
        else:
            target = dict(prompt_image=ref_image, points=pos_points)
        prompts.append(target)
    return prompts


def trex2_postprocess(
    target_image,
    trex2_results,
    visual_threshold,
    return_point,
    point_width,
    return_score,
):
    if isinstance(trex2_results, dict):
        trex2_results = [trex2_results]
    # filter based on visual threshold
    scores = np.array(trex2_results[0]["scores"])
    boxes = np.array(trex2_results[0]["boxes"])
    labels = np.array(trex2_results[0]["labels"])
    filter_mask = scores > float(visual_threshold)
    boxes = boxes[filter_mask]
    labels = labels[filter_mask]
    scores = scores[filter_mask]
    trex2_results[0]["boxes"] = boxes
    trex2_results[0]["labels"] = labels
    trex2_results[0]["scores"] = scores
    target_image = Image.fromarray(target_image)
    image_with_box = plot_boxes_to_image(
        target_image, trex2_results[0], return_point, point_width, return_score
    )[0]
    visualization = np.array(image_with_box)
    mask = None
    return visualization, len(boxes), build_annotation(boxes, mask)


def inference(
    target_image,
    interactive_input,
    generic_vp1,
    generic_vp2,
    generic_vp3,
    generic_vp4,
    generic_vp5,
    generic_vp6,
    generic_vp7,
    generic_vp8,
    visual_threshold,
    return_point,
    point_width,
    return_score,
):
    generic_vp_dict = {
        "1": generic_vp1,
        "2": generic_vp2,
        "3": generic_vp3,
        "4": generic_vp4,
        "5": generic_vp5,
        "6": generic_vp6,
        "7": generic_vp7,
        "8": generic_vp8,
    }
    # tell if generic visual prompt is empty
    generic_is_empty = True
    for _, v in generic_vp_dict.items():
        if v is not None:
            generic_is_empty = False
            break
    # We support:
    # 1. interactive visual prompt
    # 2. generic visual prompt
    if interactive_input is not None and generic_is_empty:
        prompts = pack_model_input_interactive(interactive_input)
        trex2_results = trex2.interactve_inference([prompts])
    elif interactive_input is None and not generic_is_empty:
        prompts = pack_model_input_generic(generic_vp_dict)
        trex2_results = trex2.generic_inference(target_image, prompts)
    else:
        raise gr.Error(
            "You should provide either interactive visual prompt or generic visual prompt"
        )
    visualization, num_count, coco_anno = trex2_postprocess(
        target_image,
        trex2_results,
        visual_threshold,
        return_point,
        point_width,
        return_score,
    )
    # interactive only inference
    return visualization, num_count, coco_anno


args = arg_parse()
trex2 = TRex2APIWrapper(args.trex2_api_token)
# args.device = 'cuda' if torch.cuda.is_available() else 'cpu'
# sam = sam_model_registry['vit_l'](checkpoint=args.sam_checkpoint_path)
# sam.to(device=args.device)
# sam_predictor = SamPredictor(sam)

if __name__ == "__main__":
    interactive_1 = ImagePrompter(label="1", scale=1)
    generic_vp1 = ImagePrompter(label="Generic Visual Prompt 1", scale=1)
    generic_vp2 = ImagePrompter(label="Generic Visual Prompt 2", scale=1)
    generic_vp3 = ImagePrompter(label="Generic Visual Prompt 3", scale=1)
    generic_vp4 = ImagePrompter(label="Generic Visual Prompt 4", scale=1)
    generic_vp5 = ImagePrompter(label="Generic Visual Prompt 5", scale=1)
    generic_vp6 = ImagePrompter(label="Generic Visual Prompt 6", scale=1)
    generic_vp7 = ImagePrompter(label="Generic Visual Prompt 7", scale=1)
    generic_vp8 = ImagePrompter(label="Generic Visual Prompt 8", scale=1)
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue")) as demo:
        with gr.Row():
            with gr.Column():
                with gr.Row():
                    with gr.Column():
                        target_image = gr.Image(label="Input Target Image", width=300)
                    with gr.Column():
                        with gr.Row():
                            return_point = gr.Checkbox(label="Return Point Anno")
                        with gr.Row():
                            return_score = gr.Checkbox(label="Return Score")
                        with gr.Row():
                            point_width = gr.Slider(
                                label="Line/Point Width",
                                value=5.0,
                                minimum=0.0,
                                maximum=20.0,
                                step=0.01,
                            )
                with gr.Row():
                    output_image = gr.Image(label="Output Image", width=300)
                with gr.Row():
                    num_count = gr.Textbox(
                        label="Counting Results", lines=1, show_copy_button=True
                    )
                with gr.Row():
                    coco_anno = gr.Textbox(
                        label="COCO Results",
                        lines=1,
                        max_lines=4,
                        show_copy_button=True,
                    )

            with gr.Column():
                with gr.Row():
                    interactive = gr.TabbedInterface(
                        [interactive_1], ["Interactive Visual Prompt"]
                    )
                with gr.Row():
                    generic = gr.TabbedInterface(
                        [
                            generic_vp1,
                            generic_vp2,
                            generic_vp3,
                            generic_vp4,
                            generic_vp5,
                            generic_vp6,
                            generic_vp7,
                            generic_vp8,
                        ],
                        ["1", "2", "3", "4", "5", "6", "7", "8"],
                    )
                with gr.Row():
                    visual_threshold = gr.Slider(
                        label="Visual Prompt Threshold",
                        value=0.3,
                        minimum=0.0,
                        maximum=1.0,
                        step=0.01,
                    )

                with gr.Row():
                    clean = gr.Button("Clean Inputs")
                    infer = gr.Button("Run T-Rex2🦖🦖🦖")
        clean.click(
            fn=clean_input,
            outputs=[
                interactive_1,
                generic_vp1,
                generic_vp2,
                generic_vp3,
                generic_vp4,
                generic_vp5,
                generic_vp6,
                generic_vp7,
                generic_vp8,
            ],
        )
        infer.click(
            fn=inference,
            inputs=[
                target_image,
                interactive_1,
                generic_vp1,
                generic_vp2,
                generic_vp3,
                generic_vp4,
                generic_vp5,
                generic_vp6,
                generic_vp7,
                generic_vp8,
                visual_threshold,
                return_point,
                point_width,
                return_score,
            ],
            outputs=[output_image, num_count, coco_anno],
        )
    demo.launch()
