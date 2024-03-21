import argparse
import os
from trex import TRex2APIWrapper, visualize
from PIL import Image
import numpy as np


def get_args():
    parser = argparse.ArgumentParser(description="Interactive Inference")
    parser.add_argument(
        "--token",
        type=str,
        help=
        "The token for T-Rex2 API. We are now opening free API access to T-Rex2",
    )
    parser.add_argument("--box_threshold",
                        type=float,
                        default=0.3,
                        help="The threshold for box score")
    parser.add_argument("--vis_dir",
                        type=str,
                        default="demo_vis/",
                        help="The directory for visualization")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    trex2 = TRex2APIWrapper(args.token)
    prompts = [{
        'prompt_image': 'test_images/generic_prompt1.jpg',
        'rects': [[692, 338, 725, 459]]
    }, {
        'prompt_image': 'test_images/generic_prompt2.jpg',
        'rects': [[561, 231, 634, 351]]
    }]
    embedding_url = trex2.customize_embedding(prompts)
    print(f"Customized embedding URL: {embedding_url}")
