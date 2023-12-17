from dataset import CountingDataset
from mmengine import Config

if __name__ == '__main__':
    config = Config.fromfile('CA_44_config.py')
    # get all the dataset configs
    dataset_configs = config.CA_44_configs
    # get the info or every dataset
    for k, v in dataset_configs.items():
        dataset_name = v['dataset_name']
        img_dir = v['img_dir']
        ann_file = v['ann_file']
        exampler_file = v['exampler_file']
        # create dataset
        dataset = CountingDataset(img_dir, ann_file, exampler_file)
        print(f'Number of images in {dataset_name}: {len(dataset)}')
