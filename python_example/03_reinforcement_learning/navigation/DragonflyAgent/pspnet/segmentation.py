import numpy as np
from pspnet.pspnet import PSPNet
import pspnet.utils

class Segmentation():
    def __init__(self):
        self.pspnet = PSPNet()

    def segment(self, image):
        class_scores = self.pspnet.predict(image)
        class_image = np.argmax(class_scores, axis=2)
        mapped_class_image = pspnet.utils.map_class_id(class_image)
        return mapped_class_image

    def visualize(self, class_image):
        colored_class_image = pspnet.utils.color_class_image(class_image)
        return colored_class_image
