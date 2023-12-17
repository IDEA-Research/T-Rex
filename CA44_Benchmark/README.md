# CA44-Benchmark
We introduced a counting benchmark CA-44 in T-Rex, which contains 44 datasets covering eight distinct domains. The datasets are collected from various sources, most of which are from [Roboflow](https://universe.roboflow.com/).

## Download Links
- [Baidu Netdisk](https://pan.baidu.com/s/1_8b-JwsWqBjnj_RhL6Z8Rw?pwd=gi9m)
- [Google Drive](https://drive.google.com/file/d/1iL4bgOqBHjKFWZAR6j7DSMD1zaakLD3p/view?usp=sharing)

## Browse Datasets
We also provide codes for browsing the datasets. Checkout [browse.py](CA44_Benchmark/browse.py) for simple usage. Here is a brief guide:

```bash
# 1. Download the datasets
# 2. Unzip
tar -zxvf CountAnythingV1_clean.tar.gz
# 3. Install. You need to have a basic pytorch environment.
pip install mmengine
# 4. Browse. You will get the dataset size of each subset
python browse.py
```