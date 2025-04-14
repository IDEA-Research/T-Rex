import base64
import tempfile
import time
from io import BytesIO
from typing import Dict, List, Union

import numpy as np
import requests
from PIL import Image


def encode_image(image):
    """
    Encodes an image to a base64 string.

    Args:
        image (str or PIL.Image.Image): The image to encode.
            - If str: should be a valid image file path.
            - If PIL.Image.Image: image will be encoded from memory.

    Returns:
        str: Base64-encoded image string.
    """
    if isinstance(image, str):
        # Treat as file path
        with open(image, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    elif isinstance(image, Image.Image):
        # Encode from in-memory PIL image
        buffer = BytesIO()
        image.save(buffer, format="JPEG")  # You can change to PNG if needed
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    else:
        raise TypeError("Input must be a file path (str) or PIL.Image.Image object.")


class TRex2APIWrapper:
    """API wrapper for T-Rex2

    Args:
        token (str): The token for T-Rex2 API. We are now opening free API access to T-Rex2. For
            educators, students, and researchers, we offer an API with extensive usage times to
            support your educational and research endeavors. Please send a request to this email
            address (weiliu@idea.edu.cn) and attach your usage purpose as well as your institution.
    """

    def __init__(self, token: str):
        self.headers = {"Content-Type": "application/json", "Token": token}

    def call_api(self, task_dict):
        resp = requests.post(
            url="https://api.deepdataspace.com/v2/task/trex/detection",
            json=task_dict,
            headers=self.headers,
        )
        json_resp = resp.json()
        if json_resp["msg"] != "ok":
            raise RuntimeError(f"API call failed with error: {json_resp}")
        task_uuid = json_resp["data"]["task_uuid"]

        while True:
            resp = requests.get(
                f"https://api.deepdataspace.com/v2/task_status/{task_uuid}",
                headers=self.headers,
            )
            json_resp = resp.json()
            if json_resp["data"]["status"] not in ["waiting", "running"]:
                break
            time.sleep(1)

        if json_resp["data"]["status"] == "failed":
            raise RuntimeError(f"API call failed with error: {json_resp['msg']}")
        elif json_resp["data"]["status"] == "success":
            return json_resp

    def convert_embedding_prompt(
        self, target_image: Union[str, Image.Image], base64_embedding: str
    ):
        """Convert the prompt to the format required by the API"""
        target_image_base64 = encode_image(target_image)
        prompt = {
            "model": "T-Rex-2.0",
            "image": f"data:image/jpg;base64,{target_image_base64}",
            "targets": ["bbox"],
            "prompt": {"type": "embedding", "embedding": base64_embedding},
        }
        return prompt

    def convert_visual_prompt(
        self,
        target_image: Union[str, Image.Image],
        prompts: List[Dict],
        return_type: List[str] = ["bbox"],
    ):
        """Convert the prompt to the format required by the API"""
        target_image_base64 = encode_image(target_image)

        for prompt in prompts:
            prompt["image"] = f"data:image/jpg;base64,{encode_image(prompt['image'])}"

        prompt = {
            "model": "T-Rex-2.0",
            "image": f"data:image/jpg;base64,{target_image_base64}",
            "targets": return_type,
            "prompt": {"type": "visual_images", "visual_images": prompts},
        }

        return prompt

    def visual_prompt_inference(
        self,
        target_image: Union[str, Image.Image],
        prompt: List[Dict],
        return_type: List[str] = ["bbox"],
    ):
        """Visual prompt inference for both interactive and generic workflow.

        Args:
            target_image (Union[str, Image.Image]): The image to upload. Can be a file path or PIL.Image
            prompts (List[dict]): A list of prompt dict. Each dict is for one prompt image:
                #  Box prompt
                [
                    {
                        "image": (str or Image.Image): Prompt Image 1,
                        "interactions": [
                            {
                                "type": "rect",
                                "category_id": 12,
                                "rect": [159.78119507908616, 186.52658172231986, 337.2996485061512, 309.2963532513181],
                            },
                            {
                                "type": "rect",
                                "category_id": 1,
                                "rect": [159.78119507908616, 186.52658172231986, 337.2996485061512, 309.2963532513181],
                            }
                            ... # more prompt on current image
                        ]
                    },
                    {
                        "image": (str or Image.Image): Prompt Image 2,
                        "interactions": [
                            {
                                "type": "rect",
                                "category_id": 12,
                                "rect": [159.78119507908616, 186.52658172231986, 337.2996485061512, 309.2963532513181],
                            },
                            {
                                "type": "rect",
                                "category_id": 1,
                                "rect": [159.78119507908616, 186.52658172231986, 337.2996485061512, 309.2963532513181],
                            }
                            ... # more prompt on current image
                        ]
                    }
                    ... # more prompt image.
                ]
                #  Point prompt
                [
                    {
                        "image": (str or Image.Image): Prompt Image 1,
                        "interactions": [
                            {
                                "type": "point",
                                "category_id": 12,
                                "point": [159.78119507908616, 186.52658172231986],
                            },
                            {
                                "type": "point",
                                "category_id": 1,
                                "point": [159.78119507908616, 186.52658172231986],
                            }
                            ... # more prompt on current image
                        ]
                    },
                    {
                        "image": (str or Image.Image): Prompt Image 2,
                        "interactions": [
                            {
                                "type": "point",
                                "category_id": 12,
                                "point": [159.78119507908616, 186.52658172231986],
                            },
                            {
                                "type": "point",
                                "category_id": 1,
                                "point": [159.78119507908616, 186.52658172231986],
                            }
                            ... # more prompt on current image
                        ]
                    }
                    ... # more prompt image.
                ]
            return_type (List[str]): The type of return value. Currently only support "bbox" and "embedding".

        Returns:
            detection_result (Dict): Detection result in format:
                {
                    "scores": (List[float]): A list of scores for each object in the batch
                    "labels": (List[int]): A list of labels for each object in the batch
                    "boxes": (List[List[int]]): A list of boxes for each object in the batch,
                        in format [xmin, ymin, xmax, ymax]
                }
            base64_embedding (str): The base64 encoding of the embedding. Only available when
                "embedding" is in return_type, else None

        """
        # Convert the interactive prompt to the format required by the API
        prompt = self.convert_visual_prompt(target_image, prompt, return_type)
        # call the API
        result = self.call_api(prompt)
        detection_result = self.postprocess(result["data"]["result"]["objects"])
        if "embedding" in return_type:
            base64_embedding = result["data"]["result"]["embedding"]
        else:
            base64_embedding = None
        return detection_result, base64_embedding

    def embedding_inference(
        self, target_image: Union[str, Image.Image], base64_embedding: str
    ):
        """Prompt inference workflow.
        Args:
            target_image (Union[str, Image.Image]): The image to upload. Can be a file path or PIL.Image
            base64_embedding (str): The base64 encoding of the embedding.

        Returns:
           Dict: Return dict in format:
                {
                    "scores": (torch.Tensor): Sigmoid logits in shape (batch_size, 900, num_classes),
                        class order is the same as the order in the prompt
                    "labels": (List[List[int]]): A list of list of labels for each batch image.
                    "boxes": (torch.Tensor): Normalized prediction boxes in shape (batch_size, 900, 4),
                        format is (xmin, ymin, ymin, ymax)
                }
        """
        prompt = self.convert_embedding_prompt(target_image, base64_embedding)
        result = self.call_api(prompt)
        detection_result = self.postprocess(result["data"]["result"]["objects"])
        return detection_result

    def postprocess(self, object_batches):
        """Postprocess the result from the API

        Args:
            object_batches (List[Dict]): List of Dicts. Each dict contains the prediction
                on each image. Each TRexObject contains the following keys:
                    - category_id (int): The category id of the object
                    - score (float): The score of the object
                    - bbox (List[int]): The bounding box of the object in format [xmin, ymin, xmax, ymax]

        Returns:
            List[Dict]: Return a list of dict in format:
                {
                    "scores": (List[float]): A list of scores for each object in the batch
                    "labels": (List[int]): A list of labels for each object in the batch
                    "boxes": (List[List[int]]): A list of boxes for each object in the batch
                }

        """
        scores = []
        labels = []
        boxes = []
        for obj in object_batches:
            score = obj["score"]
            category_id = obj["category_id"]
            bbox = obj["bbox"]
            scores.append(score)
            labels.append(category_id)
            boxes.append(bbox)
        return {"scores": scores, "labels": labels, "boxes": boxes}
