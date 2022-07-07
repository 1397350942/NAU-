'''
    压缩图片大小，并在原路径存储为jpeg格式
    返回：新图片的路径
'''
import pathlib
import cv2
import numpy as np


def compress_img(img_path):
    p = pathlib.Path(img_path)
    if p.exists():
        # 存储压缩完成的图片
        print("------------------------> 开始压缩图片：%s <-----------------------------" % p)

        img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
        # 根据图片宽度压缩
        if img.shape[0] >= 3000:
            img = cv2.resize(img, (0, 0), fx=0.2, fy=0.2)
        elif img.shape[0] >= 2000:
            img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)
        elif img.shape[0] >= 1000:
            img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
        elif img.shape[0] >= 800:
            img = cv2.resize(img, (0, 0), fx=0.7, fy=0.7)

        # 大小调整完毕后，保存为 jpeg 格式图片
        # 调整路径
        if img_path.split('.')[-1] != 'jpeg':
            img_path = img_path.replace(img_path.split('.')[-1], 'jpeg')
        # 存储压缩完成的图片
        print("------------------------> 压缩图片完成：%s <-----------------------------" % img_path)
        is_ok = cv2.imencode('.jpeg', img)[1].tofile(img_path)

        if is_ok:
            print("------------------------> 存储完成：%s <-----------------------------" % img_path)

        # 返回图片新路径
        return img_path

