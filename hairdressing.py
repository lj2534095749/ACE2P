"""
def segmentation(images=None,
                 paths=None,
                 batch_size=1,
                 use_gpu=False,
                 output_dir='ace2p_output',
                 visualization=False):

* images (list[numpy.ndarray]): 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
* paths (list[str]): 图片的路径；
* batch_size (int): batch 的大小；
* use_gpu (bool): 是否使用 GPU；
* output_dir (str): 保存处理结果的文件目录；
* visualization (bool): 是否将识别结果保存为图片文件。

* res (list[dict]): 识别结果的列表，列表中每一个元素为 dict，关键字有'path', 'data'，相应的取值为：
    * path (str): 原输入图片的路径；
    * data (numpy.ndarray): 图像分割得到的结果，shape 为H * W，元素的取值为0-19，表示每个像素的分类结果，映射顺序与下面的调色板相同。
"""

import cv2
import os
import imageio
import numpy as np
import paddlehub as hub
from random import randrange
import matplotlib.image as mpimg

class Ace2p:
    def __init__(self):
        # 原图片
        # image = 'awei.jpg'
        # 输出的文件夹名称
        self.output = 'output'
        # 生成多少张图片
        self.image_num = 6
        # gif的图片名
        self.gif_name = 'background.gif'
        # 自己设定颜色
        self.colors = {
            'background': '#000000',
            'hat': '#800000',
            'hair': '#008000',
            'glove': '#808000',
            'sunglasses': '#000080',
            'upperclothes': '#800080',
            'dress': '#008080',
            'coat': '#808080',
            'socks': '#400000',
            'pants': '#c00000',
            'jumpsuits': '#408000',
            'scarf': '#c08000',
            'skirt': '#400080',
            'face': '#c00080',
            'left-arm': '#408080',
            'right-arm': '#c08080',
            'left-leg': '#004000',
            'right-leg': '#804000',
            'left-shoe': '#00c000',
            'right-shoe': '#80c000',
        }

    def hairdressing(self, image):
        # os.environ['CUDA_VISIBLE_DEVICES'] = '0'

        human_parser = hub.Module(name="ace2p")
        result = human_parser.segmentation(images=[cv2.imread(image)], visualization=True, use_gpu=False)

        # 原图片
        origin = cv2.imread(image, -1)
        # 切割的图片
        path = os.path.join('ace2p_output/', result[0]['path'][0:-3] + 'png')
        mask = cv2.imread(path, -1)
        # get_random_color随机生成颜色，去掉之后即按照colors的颜色生成
        if not os.path.exists(self.output):
            os.mkdir(self.output)
        for i in range(self.image_num):
            final = self.change_color(origin, mask, 'hair', self.get_random_color())
            final = cv2.cvtColor(final, cv2.COLOR_BGRA2RGBA)
            self.save_image(i, final)

        # 需要合在一起的图片
        image_list = ['output/' + str(x) + ".png" for x in range(0, self.image_num)]

        frames = []
        for image_name in image_list:
            frames.append(imageio.imread(image_name))

        # druation : 图片切换的时间，单位秒
        imageio.mimsave(self.gif_name, frames, 'GIF', duration=0.8)

        print("Finished.............................")

    # 随机颜色
    def get_random_color(self):
        return (randrange(0, 255, 1), randrange(0, 255, 1), randrange(0, 255, 1))


    def color_str_to_list(self, color_str):
        return [int(color_str[1:3], 16), int(color_str[3:5], 16), int(color_str[5:7], 16)]


    def change_color(self, origin_img, mask_img, label, color=None):
        label_mask = mask_img.copy()
        result = origin_img.copy()
        alpha = 0.9
        label_mask[np.where((label_mask != self.color_str_to_list(self.colors[label])).any(axis=2))] = [0, 0, 0]
        if not color:
            color = self.color_str_to_list(self.colors[label])
        pos = np.where((label_mask == self.color_str_to_list(self.colors[label])).all(axis=2))

        for i, j in zip(pos[0], pos[1]):
            result[i][j] = alpha * origin_img[i][j] + (1 - alpha) * np.array(color)

        return result


    def save_image(self, i, final):
        name = os.path.join(self.output, str(i) + '.png')
        mpimg.imsave(name, final)

if __name__ == "__main__":
    my = Ace2p()
    my.hairdressing('awei.jpg')
