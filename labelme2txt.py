#!/usr/bin/python3

import os
import json
import numpy as np
import cv2

# import chardet


CLASSES = ["Dianti", "Ren"]


def convert(size, box):
    """
    input:
    size:(width,height);
    box:(x1,x2,y1,y2)
    output:
    (x,y,w,h)
    """
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = abs(box[1] - box[0])
    h = abs(box[3] - box[2])
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def json2txt(path_json, path_txt):
    # with open(path_json, 'rb') as f:
    #     result = chardet.detect(f.read())
    #     encoding = result['encoding']
    #     print(f'检测到的编码方式: {encoding}')
    # with open(path_json, "r", encoding=encoding) as path_json:
    with open(path_json, "r") as json_file:
        jsonx = json.load(json_file)
        width = int(jsonx["imageWidth"])
        height = int(jsonx["imageHeight"])
        # 获取jpg图像文件路径
        path_img = path_json.replace(".json", ".jpg")
        # 读取jpg图像
        img = cv2.imread(path_img)
        with open(path_txt, "w+") as ftxt:
            # 遍历每一个bbox对象
            for shape in jsonx["shapes"]:
                obj_cls = str(shape["label"])
                cls_id = CLASSES.index(obj_cls)
                points = np.array(shape["points"])
                x1 = int(points[0][0])
                y1 = int(points[0][1])
                x2 = int(points[1][0])
                y2 = int(points[1][1])
                # (两个角) -> (中心点,宽高) 归一化
                bb = convert((width, height), (x1, x2, y1, y2))
                print(x1, x2, y1, y2)
                print(bb[0], bb[1], bb[2], bb[3])
                print(
                    ((bb[0] - bb[2] / 2) * width, (bb[1] - bb[3] / 2) * height),
                    ((bb[0] + bb[2] / 2) * width, (bb[1] + bb[3] / 2) * height),
                )
                draw_x1 = int((bb[0] - bb[2] / 2) * width)
                draw_y1 = int((bb[1] - bb[3] / 2) * height)
                draw_x2 = int((bb[0] + bb[2] / 2) * width)
                draw_y2 = int((bb[1] + bb[3] / 2) * height)
                # 在图像上绘制边界框
                cv2.rectangle(
                    img,
                    (draw_x1,draw_y1),
                    (draw_x2,draw_y2),
                    (0, 255, 0),
                    2,
                )
                ftxt.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + "\n")

        # NOTE: debug 显示绘制了边界框的图像
        # cv2.imshow("Annotated Image", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


# json文件夹
dir_json = "./images/"

# txt文件夹
dir_txt = dir_json

if __name__ == "__main__":
    if not os.path.exists(dir_txt):
        os.makedirs(dir_txt)
    # 得到所有json文件
    list_json = os.listdir(dir_json)
    # 遍历每一个json文件,转成txt文件
    for cnt, json_name in enumerate(list_json):
        if not json_name.endswith(".json"):
            continue
        # print("name=%s" % (json_name))
        path_json = dir_json + json_name
        path_txt = dir_txt + json_name.replace(".json", ".txt")
        # (x1,y1,x2,y2)->(x,y,w,h)
        json2txt(path_json, path_txt)
        print("complete generate file name={}", path_txt)
