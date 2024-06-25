
<div align=center>
  <img src="assets/trex2/head.jpg" width=900 >
</div>

<div align=center>
  <p> A picture speaks volumes, as do the words that frame it.</p>
</div>

<div align=center>

![Static Badge](https://img.shields.io/badge/T--Rex-2-2) [![arXiv preprint](https://img.shields.io/badge/arxiv_2403.14610-blue%3Flog%3Darxiv)](https://arxiv.org/pdf/2403.14610.pdf)   [![Homepage](https://img.shields.io/badge/homepage-visit-blue)](https://deepdataspace.com/home) [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FMountchicken%2FT-Rex&count_bg=%2379C83D&title_bg=%23DF9B9B&icon=iconify.svg&icon_color=%23FFF9F9&title=VISITORS&edge_flat=false)](https://hits.seeyoufarm.com) [![Static Badge](https://img.shields.io/badge/Try_Demo!-blue?logo=chainguard&logoColor=green)](https://deepdataspace.com/playground/ivp)
</div>

----
📌 If you find our project helpful and need more API token quotas, you can request additional tokens by [filling out this form](https://docs.google.com/forms/d/e/1FAIpQLSfjogAtkgoVyFX9wvCAE15mD7QtHdKdKOrVmcE5GT1xu-03Aw/viewform?usp=sf_link). Our team will review your request and allocate more tokens for your use in one or two days. You can also apply for more tokens by sending us an email.

----
<!-- Add demo video from youtube -->
# Introduction Video 🎥 
Turn on the music if possible 🎧
<!-- Add a video here -->
[![Video Name](assets/trex2/video_cover.jpg)](https://github.com/Mountchicken/Union14M/assets/65173622/60be19f5-88e4-478e-b1a3-af62b8d6d177)

# News 📰
- **2024-06-24**: We have introduced two new free products based on T-Rex2:
  - [**Count Anything APP**](https://apps.apple.com/app/id6502489882): CountAnything is a versatile, efficient, and cost-effective counting tool that utilizes advanced computer vision algorithms, specifically T-Rex, for automated counting. It is applicable across various industries, including manufacturing, agriculture, and aquaculture.
  
[![Video Name](assets/trex2/countanything.jpg)](https://github.com/Mountchicken/Mountchicken/assets/65173622/1cffc04a-d9be-46ec-b87e-f754b71d6e21)
  
  - [**T-Rex Label**](https://www.trexlabel.com/?source=gh): T-Rex Label is an advanced annotation tool powerd by T-Rex2, specifically designed to handle the complexities of various industries and scenarios. It is the ideal choice for those aiming to streamline their workflows and effortlessly create high-quality datasets.

[![Video Name](assets/trex2/trexlabel.jpg)](https://github.com/Mountchicken/CodeCookbook/assets/65173622/58129775-533d-4aad-88f4-e1992546f9ba)

- **2024-05-17**: [Grounding DINO 1.5](https://github.com/IDEA-Research/Grounding-DINO-1.5-API) is released. This is IDEA Research's Most Capable Open-World Object Detection Model Series. It can detect any object throught text prompts!

# Contents 📜
- [Introduction Video 🎥](#introduction-video-)
- [News 📰](#news-)
- [Contents 📜](#contents-)
- [1. Introduction 📚](#1-introduction-)
  - [What Can T-Rex Do 📝](#what-can-t-rex-do-)
- [2. Try Demo 🎮](#2-try-demo-)
- [3. API Usage Examples📚](#3-api-usage-examples)
  - [Setup](#setup)
  - [Interactive Visual Prompt API](#interactive-visual-prompt-api)
  - [Generic Visual Prompt API](#generic-visual-prompt-api)
  - [Customize Visual Prompt Embedding API](#customize-visual-prompt-embedding-api)
  - [Embedding Inference API](#embedding-inference-api)
- [4. Local Gradio Demo with API🎨](#4-local-gradio-demo-with-api)
  - [4.1. Setup](#41-setup)
  - [4.2. Run the Gradio Demo](#42-run-the-gradio-demo)
  - [4.3. Basic Operations](#43-basic-operations)
- [5. Related Works](#5-related-works)
- [BibTeX 📚](#bibtex-)

# 1. Introduction 📚
Object detection, the ability to locate and identify objects within an image, is a cornerstone of computer vision, pivotal to applications ranging from autonomous driving to content moderation. A notable limitation of traditional object detection models is their closed-set nature. These models are trained on a predetermined set of categories, confining their ability to recognize only those specific categories. The training process itself is arduous, demanding expert knowledge, extensive datasets, and intricate model tuning to achieve desirable accuracy. Moreover, the introduction of a novel object category, exacerbates these challenges, necessitating the entire process to be repeated.

T-Rex2 addresses these limitations by integrating both text and visual prompts in one model, thereby harnessing the strengths of both modalities. The synergy of text and visual prompts equips T-Rex2 with robust zero-shot capabilities, making it a versatile tool in the ever-changing landscape of object detection.
<!-- insert image in the middle -->
<div align=center>
  <img src="assets/trex2/method.jpg" width=600 >
</div>

## What Can T-Rex Do 📝
T-Rex2 is well-suited for a variety of real-world applications, including but not limited to: agriculture, industry, livstock and wild animals monitoring, biology, medicine, OCR, retail, electronics, transportation, logistics, and more. T-Rex2 mainly supports three major workflows including interactive visual prompt workflow, generic visual prompt workflow and text prompt workflow. It can cover most of the application scenarios that require object detection

[![Video Name](assets/trex2/video_cover2.png)](https://github.com/Mountchicken/Union14M/assets/65173622/c3585d49-208c-4ba4-9954-fd1572d299dc)

# 2. Try Demo 🎮
We are now opening online demo for T-Rex2. [Check our demo here](https://deepdataspace.com/playground/ivp)

<div align=center>
  <img src="assets/trex2/demo.jpg">
</div>


# 3. API Usage Examples📚
We are now opening free API access to T-Rex2. For educators, students, and researchers, we offer an API with extensive usage times to support your educational and research endeavors. You can get API at here [request API](https://deepdataspace.com/request_api).
- [Full API documentation can be found here](https://cloudapi-sdk.deepdataspace.com/dds_cloudapi_sdk/tasks/trex_interactive.html).


## Setup
Install the API package and acquire the API token from the email.
```bash
git clone https://github.com/IDEA-Research/T-Rex.git
cd T-Rex
pip install dds-cloudapi-sdk==0.1.1
pip install -v -e .
```



## Interactive Visual Prompt API
- In interactive visual prompt workflow, users can provide visual prompts in boxes or points format on a given image to specify the object to be detected. 

  ```python
  python demo_examples/interactive_inference.py --token <your_token> 
  ```
  - You are supposed get the following visualization results at `demo_vis/`
    <div align=center>
      <img src="assets/trex2/interactive_0.jpg" width=400 >
      <img src="assets/trex2/interactive_1.jpg" height=285 >
    </div>

## Generic Visual Prompt API
- In generic visual prompt workflow, users can provide visual prompts on one reference image
and detect on the other image.

  ```python
  python demo_examples/generic_inference.py --token <your_token> 
  ```
  - You are supposed get the following visualization results at `demo_vis/`
    <div align=center>
      <img src="assets/trex2_api_examples/generic_prompt1.jpg" width=280 > +
      <img src="assets/trex2_api_examples/generic_prompt2.jpg" width=280 > =
      <img src="assets/trex2/generic.jpg" width=280 >
    </div>

## Customize Visual Prompt Embedding API
In this workflow, you cam customize a visual embedding for a object category using multiple images. With this embedding, you can detect on any images.

  ```python
  python demo_examples/customize_embedding.py --token <your_token> 
  ```
  - You are supposed to get a download link for this visual prompt embedding in `safetensors` format. Save it and let's use it for `embedding_inference`.
  
## Embedding Inference API
With the visual prompt embeddings generated from the previous API. You can use it detect on any images.
  ```python
    python demo_examples/embedding_inference.py --token <your_token> 
  ```

# 4. Local Gradio Demo with API🎨
<div align=center>
  <img src="assets/trex2/gradio.jpg" width=500>
</div>

## 4.1. Setup
- Install T-Rex2 API if you haven't done so
```bash
- install gradio and other dependencies
```bash
# install gradio and other dependencies
pip install gradio==4.22.0
pip install gradio-image-prompter
```

## 4.2. Run the Gradio Demo
```bash
python gradio_demo.py --trex2_api_token <your_token>
```

## 4.3. Basic Operations
- **Draw Box**: Draw a box on the image to specify the object to be detected. Drag the left mouse button to draw a box.
- **Draw Point**: Draw a point on the image to specify the object to be detected. Click the left mouse button to draw a point.
- **Interactive Visual Prompt**: Provide visual prompts in boxes or points format on a given image to specify the object to be detected. The Input Target Image and Interactive Visual Prompt Image should be the same
- **Generic Visual Prompt**: Provide visual prompts on multiple reference images and detect on the other image.

# 5. Related Works
:fire: We release the [training and inference code](https://github.com/UX-Decoder/DINOv) and [demo link](http://semantic-sam.xyzou.net:6099/) of [DINOv](https://arxiv.org/pdf/2311.13601.pdf), which can handle in-context **visual prompts** for open-set and referring detection & segmentation. Check it out!

# BibTeX 📚
```
@misc{jiang2024trex2,
      title={T-Rex2: Towards Generic Object Detection via Text-Visual Prompt Synergy}, 
      author={Qing Jiang and Feng Li and Zhaoyang Zeng and Tianhe Ren and Shilong Liu and Lei Zhang},
      year={2024},
      eprint={2403.14610},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```
