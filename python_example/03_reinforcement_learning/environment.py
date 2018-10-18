import gym
import numpy as np
from VividGym import VividEnv
import json

with open('config.json', 'r') as f:
    config = json.load(f)

def create_env(env_id, channel_first=True):
    params = {k: v for k, v in config.items()}
    params['port'] = params['port'] + env_id
    env = VividEnv(**params)
    if channel_first:
        env = TorchWrapper(env)
    print('Environment {} created'.format(env_id))
    return env

class TorchWrapper(gym.ObservationWrapper):
    def __init__(self, env):
        super(TorchWrapper, self).__init__(env)
        self.observation_space = gym.spaces.Box(
            low=0, high=255,
            shape=(3, env.screen_height, env.screen_width),
            dtype=np.float32);

    def observation(self, observation):
        # convert to channel_first
        return observation.transpose(2, 0, 1).astype(np.float32)
