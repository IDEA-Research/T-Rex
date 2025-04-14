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
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    trex2 = TRex2APIWrapper(args.token)

    target_image = "assets/trex2_api_examples/generic_target.jpg"
    prompts = [
        dict(
            image="assets/trex2_api_examples/generic_prompt1.jpg",
            interactions=[
                {
                    "type": "rect",
                    "category_id": 1,
                    "rect": [692, 338, 725, 459],
                },
                {
                    "type": "rect",
                    "category_id": 1,
                    "rect": [561, 231, 634, 351],
                },
            ],
        ),
        dict(
            image="assets/trex2_api_examples/generic_prompt2.jpg",
            interactions=[
                {
                    "type": "rect",
                    "category_id": 1,
                    "rect": [561, 231, 634, 351],
                },
            ],
        ),
    ]
    result = trex2.visual_prompt_inference(
        target_image, prompts, return_type=["embedding"]
    )[1]
    # save this base64 result to a file
    with open("demo_examples/football_player_embedding.txt", "w") as f:
        f.write(result)
