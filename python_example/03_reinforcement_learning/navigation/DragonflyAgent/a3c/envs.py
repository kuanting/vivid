import gym
import numpy as np
from gym.spaces.box import Box
from dragonfly.DragonflyGym import DragonflyEnv
from pspnet.segmentation import Segmentation
from pspnet import utils as utils
import json

with open('settings.json', 'r') as f:
    settings = json.load(f)

def create_unreal_env(env_id, segmentation=True, fake=False):
    if segmentation:
        env = SegmentedEnv(fake=fake, ip=settings['ip'],
                           port=settings['port'] + env_id)
    else:
        env = NormalEnv(fake=fake, ip=settings['ip'],
                        port=settings['port'] + env_id)
    if not fake:
        print('Environment {} created'.format(env_id))
    return env


class SegmentedEnv(DragonflyEnv):
    def __init__(self, fake=False, **kwargs):
        super(SegmentedEnv, self).__init__(fake=fake, **kwargs)
        self.num_classes = len(utils.labels)
        self.observation_space = gym.spaces.Box(
            0, 255, shape=(self.num_classes, self.screen_height, self.screen_width));
        if not fake:
            self.segmentation = Segmentation()

    def observe(self):
        observation = super(SegmentedEnv, self).observe()
        class_image = self.segmentation.segment(observation)
        one_hot_image = np.eye(self.num_classes)[class_image.reshape(-1)]\
            .reshape(self.screen_height, self.screen_width, self.num_classes)
        return one_hot_image.transpose(2, 0, 1).astype(np.float32)

class NormalEnv(DragonflyEnv):
    def __init__(self, fake=False, **kwargs):
        super(NormalEnv, self).__init__(fake=fake, **kwargs)
        self.observation_space = gym.spaces.Box(
            0, 255, shape=(3, self.screen_height, self.screen_width));

    def observe(self):
        observation = super(NormalEnv, self).observe()
        return observation.transpose(2, 0, 1).astype(np.float32)
