from collections import namedtuple
import numpy as np

Label = namedtuple('Label', [
    'name',
    'id',
    'color'
])

labels = [Label('wall', 0, (218, 218, 218)),
        Label('floor', 1, (255, 0, 0)),
        Label('ceiling', 2, (0, 255, 0)),
        Label('toilet', 3, (255, 255, 0)),
        Label('other', 4, (0, 0, 255))]

id2label = {label.id: label for label in labels}
id_mapping = {id: 4 for id in range(150)}
id_mapping[0] = 0
id_mapping[3] = 1
id_mapping[5] = 2
id_mapping[65] = 3

def color_class_image(class_id_image):
    """Map the class image to a rgb-color image."""
    colored_image = np.zeros((class_id_image.shape[0], class_id_image.shape[1], 3), np.uint8)
    for row in range(class_id_image.shape[0]):
        for col in range(class_id_image.shape[1]):
            try:
                colored_image[row, col, :] = id2label[int(class_id_image[row, col])].color
            except KeyError as key_error:
                print("Warning: could not resolve classid %s" % key_error)
    return colored_image

def map_class_id(class_id_image):
    mapped_image = np.zeros((class_id_image.shape[0], class_id_image.shape[1]), np.uint8)
    for row in range(class_id_image.shape[0]):
        for col in range(class_id_image.shape[1]):
            try:
                mapped_image[row, col] = id_mapping[int(class_id_image[row, col])]
            except KeyError as key_error:
                print("Warning: could not resolve classid %s" % key_error)
    return mapped_image
