import json
import os
from typing import Dict, Union

import torch
import torch.utils.data
import torchvision


class COCOBase(torchvision.datasets.CocoDetection):
    """A dataset class for COCO-like datasets.

    Args:
        img_folder (str): The path to the folder containing the images.
        ann_file (str): The path to the annotation file.
    """

    def __init__(self, img_folder: str, ann_file: str):
        super(COCOBase, self).__init__(img_folder, ann_file)
        self.img_dir = img_folder
        self.ann_file = ann_file

    def __getitem__(self, idx) -> Union[torch.Tensor, Dict]:
        """Get a sample from the dataset.

        Args:
            idx (int): The index of the sample.

        Returns:
            img (torch.Tensor): The image.
            target (dict): Annotations in coco format

        """
        img, target = super(COCOBase, self).__getitem__(idx)
        return img, target


class CountingDataset(COCOBase):
    """A dataset wrapper for counting like dataset. Typically it should provide two annotaion 
    file. One is in classical coco format. The other is exampler in the following json format:
        {
            "0001.jpg": [[12,34,16,23], [52,32, 52, 52]],
            "0002.jpg": [[12,34,16,23], [52,32, 52, 52]],
            "0002.jpg": [[12,34,16,23], [52,32, 52, 52]]
        }
    which is a mapping from image name to a list of exampler bounding boxes. Each box is in 
    coco's xywh format.

    Args:
        image_set (str): image set name
        img_dir (str): image directory
        ann_file (str): annotation file path
        exampler_file (str): exampler file path
    """

    def __init__(self,
                 img_dir: str,
                 ann_file: str,
                 exampler_file: str = None,
                 **kwargs):

        super().__init__(img_dir, ann_file)
        self.img_dir = img_dir
        # load exampler file
        if exampler_file:
            self.exampler_map = json.load(open(exampler_file, 'r'))
        else:
            self.exampler_map = None

    def __getitem__(self, idx) -> Union[torch.Tensor, Dict]:
        """Get a sample from the dataset.

        Args:
            idx (int): The index of the sample.

        Returns:
            img (torch.Tensor): The image.
            target (dict): COCO annotations
        """
        img, target = super(COCOBase, self).__getitem__(idx)
        image_id = self.ids[idx]
        coco_img = self.coco.loadImgs(image_id)[0]
        filename = coco_img["file_name"]
        if self.exampler_map:
            exampler_box = self.exampler_map[filename]
        else:
            exampler_box = None
        target = {
            "image_id": image_id,
            "image_path": os.path.join(self.img_dir, coco_img["file_name"]),
            "annotations": target,
            "exampler_box": exampler_box,
        }
        return img, target
