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
        'image':
        'test_images/interactive1.jpeg',
        'prompts': [{
            'category_id': 1,
            'embd': 'test_images/football_player.safetensors'
        }, {
            'category_id': 2,
            'embd': 'test_images/pigeon.safetensors'
        }]
    }]
    results = trex2.embedding_inference(prompts)
    # filter out the boxes with low score
    filtered_results = []
    for result in results:
        scores = np.array(result['scores'])
        labels = np.array(result['labels'])
        boxes = np.array(result['boxes'])
        filter_mask = scores > args.box_threshold
        filtered_result = {
            'scores': scores[filter_mask],
            'labels': labels[filter_mask],
            'boxes': boxes[filter_mask]
        }
        filtered_results.append(filtered_result)
    # visualize the results
    if not os.path.exists(args.vis_dir):
        os.makedirs(args.vis_dir)
    for i, (prompt, result) in enumerate(zip(prompts, filtered_results)):
        image_path = prompt['image']
        image = Image.open(image_path)
        image = visualize(image, result, draw_score=True)
        image.save(os.path.join(args.vis_dir, f"embedding_inference_{i}.jpg"))
        print(
            f"Visualized image saved to {args.vis_dir}/embedding_inference_{i}.jpg"
        )
