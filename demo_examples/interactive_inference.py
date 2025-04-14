import argparse
import os

import numpy as np
from PIL import Image

from trex import TRex2APIWrapper, visualize


def get_args():
    parser = argparse.ArgumentParser(description="Interactive Inference")
    parser.add_argument(
        "--token",
        type=str,
        help="The token for T-Rex2 API. We are now opening free API access to T-Rex2",
    )
    parser.add_argument(
        "--box_threshold", type=float, default=0.3, help="The threshold for box score"
    )
    parser.add_argument(
        "--vis_dir",
        type=str,
        default="demo_vis/",
        help="The directory for visualization",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    trex2 = TRex2APIWrapper(args.token)
    # demo for box input
    target_image = "assets/trex2_api_examples/interactive1.jpeg"
    prompts = [
        dict(
            image="assets/trex2_api_examples/interactive1.jpeg",
            interactions=[
                {
                    "type": "rect",
                    "category_id": 1,
                    "rect": [347, 1259, 600, 1437],
                },
                {
                    "type": "rect",
                    "category_id": 1,
                    "rect": [1085, 1154, 1154, 1246],
                },
                {
                    "type": "rect",
                    "category_id": 2,
                    "rect": [1465, 787, 1497, 877],
                },
            ],
        )
    ]

    result = trex2.visual_prompt_inference(target_image, prompts)[0]
    # filter out the boxes with low score

    scores = np.array(result["scores"])
    labels = np.array(result["labels"])
    boxes = np.array(result["boxes"])
    filter_mask = scores > args.box_threshold
    filtered_result = {
        "scores": scores[filter_mask],
        "labels": labels[filter_mask],
        "boxes": boxes[filter_mask],
    }
    # visualize the results
    if not os.path.exists(args.vis_dir):
        os.makedirs(args.vis_dir)

    image = Image.open(target_image)
    image = visualize(image, filtered_result, draw_score=True)
    image.save(os.path.join(args.vis_dir, f"interactive.jpg"))
    print(f"Visualized image saved to {args.vis_dir}/interactive.jpg")
