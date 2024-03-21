from typing import Dict

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def visualize(image_pil: Image,
              target: Dict,
              return_point: bool = False,
              draw_width: float = 6.0,
              random_color: bool = True,
              overwrite_color: Dict = None,
              agnostic_random_color: bool = False,
              draw_score=False,
              draw_label=True) -> Image:
    """Plot bounding boxes and labels on an image.

    Args:
        image_pil (PIL.Image): The input image as a PIL Image object.
        model_targetoutput (Dict[str, Union[torch.Tensor, List[torch.Tensor]]]): The target dictionary containing
            the bounding boxes and labels. The keys are:
                - boxes (List[int]): A list of bounding boxes in shape (N, 4), [x1, y1, x2, y2] format.
                - scores (List[float]): A list of scores for each bounding box. shape (N)
                - labels (List[str]): A list of string labels for each bounding box. shape (N)
        return_point (bool): Draw center point instead of bounding box. Defaults to False.
        draw_width (float): The width of the drawn bounding box or point. Defaults to 1.0.
        random_color (bool): Use random color for each category. Defaults to True.
        overwrite_color (Dict): Overwrite color for each category. Defaults to None.
        agnostic_random_color (bool): If True, we will use random color for all boxes.
        draw_score (bool): Draw score on the image. Defaults to False.

    Returns:
        Union[PIL.Image, PIL.Image]: A tuple containing the input image and ploted image.
    """
    # Get the bounding boxes and labels from the target dictionary
    boxes = target["boxes"]
    scores = target["scores"]
    labels = target["labels"]

    label2color = {}
    if overwrite_color:
        label2color = overwrite_color
    else:
        # find all unique labels
        unique_labels = set(labels)
        # generate random color for each label
        for label in unique_labels:
            if random_color:
                label2color[str(label)] = tuple(
                    np.random.randint(0, 255, size=3).tolist())
            else:
                label2color[str(label)] = (255, 255, 255)

    # Create a PIL ImageDraw object to draw on the input image
    draw = ImageDraw.Draw(image_pil)
    # Create a new binary mask image with the same size as the input image
    mask = Image.new("L", image_pil.size, 0)
    # Create a PIL ImageDraw object to draw on the mask image
    mask_draw = ImageDraw.Draw(mask)

    # Draw boxes and masks for each box and label in the target dictionary
    for box, score, label in zip(boxes, scores, labels):
        # Convert the box coordinates from 0..1 to 0..W, 0..H
        score = score.item()
        if not agnostic_random_color:
            color = label2color[str(label)]
        else:
            color = tuple(np.random.randint(0, 255, size=3).tolist())
        # Extract the box coordinates
        x0, y0, x1, y1 = box
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        if return_point:
            ceter_x = int((x0 + x1) / 2)
            ceter_y = int((y0 + y1) / 2)
            # Draw the center point on the input image
            draw.ellipse((ceter_x - draw_width, ceter_y - draw_width,
                          ceter_x + draw_width, ceter_y + draw_width),
                         fill=color,
                         width=draw_width)
        else:
            # Draw the box outline on the input image
            draw.rectangle([x0, y0, x1, y1],
                           outline=color,
                           width=int(draw_width))

        # Draw the label text on the input image
        if not draw_label:
            label = ""
        if draw_score:
            text = f"{label} {score:.2f}"
        else:
            text = f"{label}"
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
    return image_pil
