from __future__ import print_function
from __future__ import division
from math import ceil
import numpy as np
from scipy import misc, ndimage
from .pspnet_model import _PSPNet
import torch
from torch.autograd import Variable
import torch.nn.functional as F

# These are the means for the ImageNet pretrained ResNet
DATA_MEAN = np.array([[[123.68, 116.779, 103.939]]])  # RGB order


class PSPNet(object):
    def __init__(self):
        """Instanciate a PSPNet."""

        self.model = _PSPNet(n_classes=150,
                             n_blocks=[3, 4, 6, 3],
                             pyramids=[6, 3, 2, 1])

        self.model.load_state_dict(torch.load('pspnet/models/pspnet50_ADE20K.pth'))
        self.model.eval()
        self.model.cuda()
        self.input_shape = (473, 473)

    def predict(self, img):
        """
        Predict segementation for an image.

        Arguments:
            img: must be rowsxcolsx3
        """
        h_ori, w_ori = img.shape[:2]
        if img.shape[0:2] != self.input_shape:
            img = misc.imresize(img, self.input_shape)
        input_data = self.preprocess_image(img)

        prediction = self.model(Variable(input_data, volatile=True))
        prediction = F.upsample(prediction, size=self.input_shape, mode='bilinear')
        prediction = F.softmax(prediction, dim=1)
        prediction = prediction[0].cpu().data.numpy()
        prediction = prediction.transpose(1, 2, 0)

        if img.shape[0:1] != self.input_shape:  # upscale prediction if necessary
            h, w = prediction.shape[:2]
            prediction = ndimage.zoom(prediction, (1.*h_ori/h, 1.*w_ori/w, 1.),
                                      order=1, prefilter=False)
        return prediction

    def preprocess_image(self, img):
        """Preprocess an image as input."""
        float_img = img.astype('float16')
        centered_image = float_img - DATA_MEAN
        bgr_image = centered_image[:, :, ::-1].copy().transpose(2, 0, 1)  # RGB => BGR
        input_data = torch.from_numpy(bgr_image).float().unsqueeze(0)
        input_data = input_data.cuda()
        return input_data
