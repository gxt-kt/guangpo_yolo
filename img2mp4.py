import os
import cv2
import numpy as np

def create_video_from_images(folder_path):
    # 获取文件夹中所有的jpg文件,并按文件名排序
    image_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.jpg')])
    image_paths = [os.path.join(folder_path, f) for f in image_files]

    # 获取第一张图片的尺寸
    first_image = cv2.imread(image_paths[0])
    height, width, channels = first_image.shape

    # 创建视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter('output_video.mp4', fourcc, 30.0, (width, height))

    # 逐个添加图片到视频
    for image_path in image_paths:
        print("do file ",image_path)
        image = cv2.imread(image_path)
        video_writer.write(image)

    # 释放资源
    video_writer.release()
    print("视频已成功创建!")

# 调用函数,传入图片文件夹路径
create_video_from_images("images")
