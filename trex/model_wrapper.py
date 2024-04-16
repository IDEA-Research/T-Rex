import tempfile
from typing import Dict, List, Union
import numpy as np
from dds_cloudapi_sdk import (
    BatchEmbdInfer,
    BatchEmbdPrompt,
    BatchPointInfer,
    BatchPointPrompt,
    BatchRectInfer,
    BatchRectPrompt,
    Client,
    Config,
    TRexEmbdCustomize,
    TRexEmbdInfer,
    TRexGenericInfer,
    TRexInteractiveInfer,
)
from PIL import Image


class TRex2APIWrapper:
    """API wrapper for T-Rex2

    Args:
        token (str): The token for T-Rex2 API. We are now opening free API access to T-Rex2. For
            educators, students, and researchers, we offer an API with extensive usage times to
            support your educational and research endeavors. Please send a request to this email
            address (weiliu@idea.edu.cn) and attach your usage purpose as well as your institution.
    """

    def __init__(self, token: str):
        self.client = Client(Config(token=token))

    def interactve_inference(self, prompts: List[Dict]):
        """Interactive visual prompt inference workflow. Users can provide prompt
        on current image and get the boxes, scores, labels. We take batch as input and
        each image is a dict. Note that the maximum batch size is 4.

        Args:
            prompts (List[dict]): List of batch annotations, each batch annotation is a dict:
                [
                    # Batch 1, Box prompt
                    {
                        "prompt_image": "test1.jpg",
                        "type": "rect", // rect, point
                        "prompts": [
                            {
                                "category_id": 1,
                                "rect": [[ 10, 10, 20, 30 ],[ 10, 10, 20, 30 ]] // N * [xmin, ymin, xmax, ymax],
                            },
                            {
                                "category_id": 2,
                                "rect": [[ 10, 10, 20, 30 ],[ 10, 10, 20, 30 ]] // [xmin, ymin, xmax, ymax]
                            }
                        ]
                    }
                    # Batch 2, Point prompt
                    {
                        "prompt_image": "test2.jpg",
                        "type": "point", // rect, point.
                        "prompts": [
                            {
                                "category_id": 1,
                                "point": [[ 10, 10],[ 10, 10]]  // N * [xmin, ymin, xmax, ymax],
                            },
                            {
                                "category_id": 2,
                                "point": [[ 10, 10],[ 10, 10]]  // [xmin, ymin, xmax, ymax]
                            }
                        ]
                    }
                    ...
                ]

        Returns:
            List[Dict]: Return a list of dict in format:
                [
                    {
                        "scores": (List[float]): A list of scores for each object in the batch
                        "labels": (List[int]): A list of labels for each object in the batch
                        "boxes": (List[List[int]]): A list of boxes for each object in the batch,
                            in format [xmin, ymin, xmax, ymax]
                    }
                ]
        """
        # construct input prompts
        input_prompts = []
        for prompt in prompts:
            if prompt["type"] == "rect":
                prompt = BatchRectInfer(
                    image=self.get_image_url(prompt["prompt_image"]),
                    prompts=[
                        BatchRectPrompt(
                            category_id=prompt["prompts"][i]["category_id"],
                            rects=prompt["prompts"][i]["rects"],
                        )
                        for i in range(len(prompt["prompts"]))
                    ],
                )
            elif prompt["type"] == "point":
                prompt = BatchPointInfer(
                    image=self.get_image_url(prompt["prompt_image"]),
                    prompts=[
                        BatchPointPrompt(
                            category_id=prompt["prompts"][i]["category_id"],
                            points=prompt["prompts"][i]["points"],
                        )
                        for i in range(len(prompt["prompts"]))
                    ],
                )
            else:
                assert False, "Invalid prompt type"
            input_prompts.append(prompt)
        # call the API
        task = TRexInteractiveInfer(input_prompts)
        self.client.run_task(task)
        return self.postprocess(task.result.object_batches)

    def generic_inference(self, target_image: str, prompts: List[dict]):
        """Generic visual prompt inference workflow. Users can provide prompt on multiple image and
        get the boxes, scores on target image. In generic mode, we will hypothesis that there is
        only one category per image and we do not support batch inference. Note that different
        prompt image must use the same prompt type

        Args:
            target_image (str): Path to the image file.
            prompts (List[List[dict]]): annotation in standard coco format:
                [
                    {
                        "rect": [[ 10, 10, 20, 30],[ 10, 10, 20, 30]]  // [xmin, ymin, xmax, ymax],
                        "point" (optional): [[cx, cy]]. Point and bbox can not be provided at the same time.
                        "prompt_image" (Union[str, Image.Image]): A prompt image for the target image.
                    },
                    {
                        "rect": [[ 10, 10, 40, 50],[ 20, 20, 30, 30]]  // [xmin, ymin, xmax, ymax],
                        "point" (optional): [[cx, cy]]. Point and bbox can not be provided at the same time.
                        "prompt_image" (Union[str, Image.Image]): A prompt image for the target image.
                    },
                ]

        Returns:
            List[Dict]: Return a list of dict in format:
                [
                    {
                        "scores": (List[float]): A list of scores for each object in the batch
                        "labels": (List[int]): A list of labels for each object in the batch
                        "boxes": (List[List[int]]): A list of boxes for each object in the batch,
                            in format [xmin, ymin, xmax, ymax]
                    }
                ]
        """
        input_prompts = []
        prompt_types = []
        # check prompt type
        for prompt in prompts:
            if "rects" in prompt:
                prompt_types.append("rects")
            elif "points" in prompt:
                prompt_types.append("points")
            else:
                assert False, "Invalid prompt type"
        # check if prompt type is consistent
        assert len(set(prompt_types)) == 1, "Prompt type must be consistent"
        prompt_type = prompt_types[0]
        for prompt in prompts:
            if prompt_type == "rects":
                prompt = BatchRectPrompt(
                    image=self.get_image_url(prompt["prompt_image"]),
                    rects=prompt["rects"],
                )
            elif prompt_type == "points":
                prompt = BatchPointPrompt(
                    image=self.get_image_url(prompt["prompt_image"]),
                    points=prompt["points"],
                )
            input_prompts.append(prompt)
        # call the API
        task = TRexGenericInfer(self.get_image_url(target_image), input_prompts)
        self.client.run_task(task)
        return self.postprocess([task.result.objects])[0]

    def customize_embedding(self, prompts: List[dict]):
        """Customize visual prompt embeddings. Users can provide multiple prompt images to
        get one embedding.

        Args:
            prompts (List[List[dict]]): annotation in standard coco format:
                [
                    {
                        "rect": [[ 10, 10, 20, 30],[ 10, 10, 20, 30]]  // [xmin, ymin, xmax, ymax],
                        "point" (optional): [[cx, cy]]. Point and bbox can not be provided at the same time.
                        "prompt_image" (Union[str, Image.Image]): A prompt image for the target image.
                    },
                    {
                        "rect": [[ 10, 10, 40, 50],[ 20, 20, 30, 30]]  // [xmin, ymin, xmax, ymax],
                        "point" (optional): [[cx, cy]]. Point and bbox can not be provided at the same time.
                        "prompt_image" (Union[str, Image.Image]): A prompt image for the target image.
                    },
                ]

        Returns:
           str: Return the url of the embedding, user can download the embedding from the url.
        """
        input_prompts = []
        prompt_types = []
        # check prompt type
        for prompt in prompts:
            if "rects" in prompt:
                prompt_types.append("rects")
            elif "points" in prompt:
                prompt_types.append("points")
            else:
                assert False, "Invalid prompt type"
        # check if prompt type is consistent
        assert len(set(prompt_types)) == 1, "Prompt type must be consistent"
        prompt_type = prompt_types[0]
        for prompt in prompts:
            if prompt_type == "rects":
                prompt = BatchRectPrompt(
                    image=self.get_image_url(prompt["prompt_image"]),
                    rects=prompt["rects"],
                )
            elif prompt_type == "points":
                prompt = BatchPointPrompt(
                    image=self.get_image_url(prompt["prompt_image"]),
                    points=prompt["points"],
                )
            input_prompts.append(prompt)
        # call the API
        task = TRexEmbdCustomize(batch_prompts=input_prompts)
        self.client.run_task(task)
        embd_url = task.result.embd
        return embd_url

    def embedding_inference(self, prompts: List[dict]):
        """Prompt inference workflow. Users can provide prompt in safetensor format
        on current image and get the boxes, scores, labels on current image. We take
        batch as input and each image is a dict. Note that the maximum batch size is 4.

        Args:
            prompts (List[dict]): List of batch annotations, each batch annotation is a dict:
                [
                    # Batch 1
                    {
                        "image": "test1.jpg",
                        "prompts": [
                            {
                                "category_id": 1,
                                "embd": "cate1.safetenosrs",
                            },
                            {
                                "category_id": 2,
                                "embd": "cate2.safetenosrs",
                            }
                        ]
                    }
                    # Batch 2
                    {
                        "image": "test2.jpg",
                        "prompts": [
                            {
                                "category_id": 1,
                                "embd": "cate1.safetenosrs",
                            },
                            {
                                "category_id": 2,
                                "embd": "cate2.safetenosrs",
                            }
                        ]
                    }
                    ...
                ]

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
        # construct input prompts
        input_prompts = []
        for prompt in prompts:
            prompt = BatchEmbdInfer(
                image=self.get_image_url(prompt["image"]),
                prompts=[
                    BatchEmbdPrompt(
                        category_id=prompt["prompts"][i]["category_id"],
                        embd=self.get_image_url(prompt["prompts"][i]["embd"]),
                    )
                    for i in range(len(prompt["prompts"]))
                ],
            )
            input_prompts.append(prompt)
        # call the API
        task = TRexEmbdInfer(input_prompts)
        self.client.run_task(task)
        return self.postprocess(task.result.object_batches)

    def postprocess(self, object_batches):
        """Postprocess the result from the API

        Args:
            object_batches (List[List[TRexObject]]): List of Lists. Each list contains the prediction
                on each image. Each TRexObject contains the following keys:
                    - category_id (int): The category id of the object
                    - score (float): The score of the object
                    - bbox (List[int]): The bounding box of the object in format [xmin, ymin, xmax, ymax]

        Returns:
            List[Dict]: Return a list of dict in format:
                [
                    {
                        "scores": (List[float]): A list of scores for each object in the batch
                        "labels": (List[int]): A list of labels for each object in the batch
                        "boxes": (List[List[int]]): A list of boxes for each object in the batch
                    }
                ]
        """
        results = []
        for batch in object_batches:
            scores = []
            labels = []
            boxes = []
            for obj in batch:
                scores.append(obj.score)
                if hasattr(obj, "category_id"):
                    labels.append(obj.category_id)
                else:
                    # generic inference does not return category_id
                    labels.append(0)
                boxes.append(obj.bbox)
            results.append({"scores": scores, "labels": labels, "boxes": boxes})
        return results

    def get_image_url(self, image: Union[str, np.ndarray]):
        """Upload Image to server and return the url

        Args:
            image (Union[str, np.ndarray]): The image to upload. Can be a file path or np.ndarray.
                If it is a np.ndarray, it will be saved to a temporary file.

        Returns:
            str: The url of the image
        """
        if isinstance(image, str):
            url = self.client.upload_file(image)
        else:
            with tempfile.NamedTemporaryFile(delete=True, suffix=".png") as tmp_file:
                # image is in numpy format, convert to PIL Image
                image = Image.fromarray(image)
                image.save(tmp_file, format="PNG")
                tmp_file_path = tmp_file.name
                url = self.client.upload_file(tmp_file_path)
        return url
