
<div align=center>
  <img src="assets/TRex.png" width=900 >
</div>

<div align=center>
  <p> A picture is worth a thousand words.</p>
</div>

<div align=center>

![Static Badge](https://img.shields.io/badge/T--Rex-Alpha-1) [![arXiv preprint](https://img.shields.io/badge/arxiv_2311.13596-blue?logo=arxiv)](https://arxiv.org/abs/2311.13596) [![Homepage](https://img.shields.io/badge/homepage-visit-blue)](https://TRex-counting.github.io/) [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FMountchicken%2FT-Rex&count_bg=%2379C83D&title_bg=%23DF9B9B&icon=iconify.svg&icon_color=%23FFF9F9&title=VISITORS&edge_flat=false)](https://hits.seeyoufarm.com)

[![video](https://img.shields.io/badge/Watch_Video-red?logo=youtube)](https://www.youtube.com/watch?v=engIEhZogAQ) [![Static Badge](https://img.shields.io/badge/Try_Demo!-blue?logo=chainguard&logoColor=green)](https://deepdataspace.com/playground/ivp)
</div>

<!-- insert a gif here -->
<div align=center>
  <img src="assets/TRex.gif" width=800 >
</div>

----


<!-- Add demo video from youtube -->
# Introduction Video 🎥
<!-- Add a video here -->
[![Video Name](assets/cover.jpeg)](https://github.com/Mountchicken/Union14M/assets/65173622/6ca0b8c3-89dd-4b33-84f3-08b2c6a3bb29)

# What is T-Rex 🦖
- T-Rex is an interactive object counting model that can first detect then count any objects through visual prompting, which is highlighted by the following features:
  - **Open-Set**: T-Rex possess the capacity to count any object, without constraints on predefined categories.
  - **Visual Promptable**: Users can provide visual examples to specify the objects for counting.
  - **Intuitive Visual Feedback**: T-Rex is a detection-based model that allows for intuitive visual feedback (i.e. detected boxes), enabling users to assess the accuracy of the result.
  - **Interactive**: Users can actively participate in the counting process to rectify errors.

<!-- insert image in the middle -->
<div align=center>
  <img src="assets/about-img.png" width=400 >
</div>

# News :rocket:
:fire: We release the [training and inference code](https://github.com/UX-Decoder/DINOv) of [DINOv](https://arxiv.org/pdf/2311.13601.pdf), which can handle in-context **visual prompts** for open-set and referring detection & segmentation. Check it out!

# How Does T-Rex Work ⚙️
- T-Rex provides three major workflows for interactive object counting / detection.
  - **Positive-only Prompt Mode**: T-Rex can detect then count similar objects in an image with just a single click or box drawing. Additional visual prompts can also be added for densely packed or small objects
  - **Positive with Negative Prompt Mode**: To address false detections caused by similar objects, users can correct the detection results by adding negative prompts to the falsely-detected objects.
  - **Cross Image Prompt Mode**: This feature supports counting across different reference and target images, ideal for automatic annotation. Users only need to prompt on one reference image, and T-Rex will detect objects in other target images. ***Note that this feature is still under development, and the performance is not guaranteed.***

<div align=center>
  <img src="assets/workflow.png" width=700 >
</div>

# What Can T-Rex Do 📝
- T-Rex can be applyed to various domains for detection/counting including but not limited to Agriculture, Industry, Livestock, Biology, Medicine, Retail, Electronic, Transportation, Logistics, Human, etc. 
- T-Rex can also serve as an open-set object detector, which can be applied for automatic annotation. It process exponential zero-shot detection capability, and offers strong performance in dense and overlapping scenes.
- We list some of the potential applications of T-Rex below:

<!-- There image each row -->
<div align=center>
  <img src="assets/1.png" width=240 >
  <img src="assets/2.png" width=240 >
  <img src="assets/3.png" width=240 >
</div>
<div align=center>

  <img src="assets/5.png" width=240 >
  <img src="assets/6.png" width=240 >
  <img src="assets/7.png" width=240 >
</div>


# Try Demo 🚀
- [https://deepdataspace.com/playground/ivp](https://deepdataspace.com/playground/ivp)
  - ⚠️ For now, the demo only support **box prompt mode**. We will add more features in the future.
![demo](assets/demo.jpeg)

# CA-44 Benchmark 📊
- [CA-44 Benchmark](CA44_Benchmark/README.md)

# BibTeX 📚
```
@misc{jiang2023trex,
      title={T-Rex: Counting by Visual Prompting}, 
      author={Qing Jiang and Feng Li and Tianhe Ren and Shilong Liu and Zhaoyang Zeng and Kent Yu and Lei Zhang},
      year={2023},
      eprint={2311.13596},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```
