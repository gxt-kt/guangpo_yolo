import os
import shutil
import random


def split_dataset(input_folder, output_folder, train_ratio=0.8):
    """
    将输入文件夹中的图像和标签文件随机分割成训练集和验证集,并保存到指定的输出文件夹中。

    参数:
    input_folder (str): 包含图像和标签文件的输入文件夹路径
    output_folder (str): 输出文件夹的上层路径
    train_ratio (float): 训练集的比例,范围为 0 到 1
    """
    # 创建输出目录
    train_img_dir = os.path.join(output_folder, "images", "train")
    train_label_dir = os.path.join(output_folder, "labels", "train")
    val_img_dir = os.path.join(output_folder, "images", "val")
    val_label_dir = os.path.join(output_folder, "labels", "val")

    os.makedirs(train_img_dir, exist_ok=True)
    os.makedirs(train_label_dir, exist_ok=True)
    os.makedirs(val_img_dir, exist_ok=True)
    os.makedirs(val_label_dir, exist_ok=True)

    # 获取图像和标签文件列表
    img_files = [f for f in os.listdir(input_folder) if f.endswith(".jpg")]
    label_files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]

    # 确保每个图像都有对应的标签文件
    print("img_files size:", len(img_files))
    print("label_files size:", len(label_files))
    # assert len(img_files) == len(label_files)

    # 使用示# 创建图像和标签文件的映射关系
    img_to_label = {}
    for img_file in img_files:
        label_file = os.path.splitext(img_file)[0] + ".txt"
        if label_file in label_files:
            img_to_label[img_file] = label_file

    # 打乱文件顺序
    file_pairs = list(img_to_label.items())
    random.shuffle(file_pairs)
    print("file_pairs size:", len(file_pairs))

    # 划分训练集和验证集
    train_size = int(len(file_pairs) * train_ratio)
    train_pairs = file_pairs[:train_size]
    val_pairs = file_pairs[train_size:]

    # 复制文件到输出目录
    for img_file, label_file in train_pairs:
        shutil.copy(
            os.path.join(input_folder, img_file), os.path.join(train_img_dir, img_file)
        )
        shutil.copy(
            os.path.join(input_folder, label_file),
            os.path.join(train_label_dir, label_file),
        )

    for img_file, label_file in val_pairs:
        shutil.copy(
            os.path.join(input_folder, img_file), os.path.join(val_img_dir, img_file)
        )
        shutil.copy(
            os.path.join(input_folder, label_file),
            os.path.join(val_label_dir, label_file),
        )

    print(f"训练集数量: {len(train_pairs)}")
    print(f"验证集数量: {len(val_pairs)}")


split_dataset("images", "output")
