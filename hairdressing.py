import cv2
import os
import imageio
import numpy as np
import paddlehub as hub
from random import randrange
import matplotlib.image as mpimg

class Ace2p:
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
        """获得经过染发后的图像

        :param image: 想要进行染发的图像
        :return: 返回已经进行染发的图像
        """

        # os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # 选择使用哪块GPU

        human_parser = hub.Module(name="ace2p")  # 调用ACE2P模型
        result = human_parser.segmentation(images=[cv2.imread(image)], visualization=True, use_gpu=False)  # 得到模型预测结果

        origin = cv2.imread(image, -1)  # 原图片
        path = os.path.join('ace2p_output/', result[0]['path'][0:-3] + 'png')  # 分割的图片的路径
        mask = cv2.imread(path, -1)  # 读取分割的图片

        if not os.path.exists(self.output):  # 如果存放结果的文件夹不存在
            os.mkdir(self.output)  # 新建一个存放结果的文件夹

        for i in range(self.image_num):
            final = self.change_color(origin, mask, 'hair', self.get_random_color())  # 修改头发颜色
            final = cv2.cvtColor(final, cv2.COLOR_BGRA2RGBA)  # BGR TO RGB
            self.save_image(i, final)  # 保存图像

        image_list = ['output/' + str(x) + ".png" for x in range(0, self.image_num)]  # 需要生成 gif 的图片

        frames = []  # 存放染发后生成的图像，用作生成 gif 文件
        for image_name in image_list:
            frames.append(imageio.imread(image_name))

        # 生成 gif 文件
        # druation : 图片切换的时间，单位秒
        imageio.mimsave(self.gif_name, frames, 'GIF', duration=0.8)

        print("Finished.............................")

    def get_random_color(self):
        """生成随机颜色

        :return 随机三通道颜色
        """

        return (randrange(0, 255, 1), randrange(0, 255, 1), randrange(0, 255, 1))

    def color_str_to_list(self, color_str):
        """将#000000颜色表示转成[00, 00, 00]

        :return 颜色三通道的十六进制表示[00, 00, 00]
        """

        return [int(color_str[1:3], 16), int(color_str[3:5], 16), int(color_str[5:7], 16)]

    def change_color(self, origin_img, mask_img, label, color=None):
        """改变颜色

        :param origin_img: 原始图像
        :param mask_img: 蒙版图像
        :param label: 选择要修改颜色的位置
        :param color: 选择要修改的颜色

        :return 修改完颜色的图片
        """

        label_mask = mask_img.copy()  # 复制蒙板图像
        result = origin_img.copy()  # 复制原始图像
        alpha = 0.9

        # 蒙板只保留头发位置，其他像素值全部为0
        label_mask[np.where((label_mask != self.color_str_to_list(self.colors[label])).any(axis=2))] = [0, 0, 0]

        # 如果设置了颜色，修改为规定格式的颜色表示
        if not color:
            color = self.color_str_to_list(self.colors[label])

        # 蒙板中除头发外的位置信息
        pos = np.where((label_mask == self.color_str_to_list(self.colors[label])).all(axis=2))

        # 原始图像与蒙板图像相加
        for i, j in zip(pos[0], pos[1]):
            result[i][j] = alpha * origin_img[i][j] + (1 - alpha) * np.array(color)

        return result

    def save_image(self, i, final):
        """保存图像

        :param i: 图像名称
        :param final: 图像
        :return:
        """

        name = os.path.join(self.output, str(i) + '.png')  # 图像保存位置
        mpimg.imsave(name, final)  # 保存图像

if __name__ == "__main__":
    my = Ace2p()
    my.hairdressing('awei.jpg')
