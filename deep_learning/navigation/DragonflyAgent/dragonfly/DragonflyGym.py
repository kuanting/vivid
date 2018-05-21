# Implement OpenAI Gym interface
import gym
from gym import spaces
import numpy as np
from dragonfly.DragonflyClient import *
import time
import msgpackrpc

class DfActionSpace:
    no_action = 0
    up = 1 
    down = 2
    turn_right = 3
    turn_left = 4

class DragonflyEnv:

    # Define moving distance or turning degree
    # This is the safe distance before hitting a obstacle
    move_distance = 50 # cm
    up_distance = 20 # cm
    turn_degree = 20 # degree
    screen_width = 256
    screen_height = 144
    done = False

    def __init__(self, fake=False, **kwargs):
        self.action_space = gym.spaces.Discrete(5) 
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(self.screen_height, self.screen_width, 3));
        # Connect to Dragonfly mode
        self.config = kwargs
        if not fake:
            self.reconnect()

    def reset(self):
        self.client.reset() 
        self.done = False
        self.distance_moved = 0
        self.max_distance = 0
        self.current_degree = 0
        self.episode_length = 0
        return self.observe()

    def reconnect(self):
        while True:
            try:
                self.client = DragonflyClient(**self.config)
                self.client.reset()
                break
            except msgpackrpc.error.TimeoutError:
                print('Connect to port {} failed, retry after 5 seconds...'.\
                      format(self.config['port']))
                time.sleep(5)
        time.sleep(1)

    def render(self):
        return self.state

    def seed(self, seed):
        pass

    def observe(self):
        # Get uncompressed screenshot from Camera 0
        resp = self.client.simGetImages([ImageRequest(0, AirSimImageType.Scene, False, False)])
        # Remove Alpha
        img_rgb = np.array(bytearray(resp[0].image_data_uint8))\
            .reshape(self.screen_height, self.screen_width, 4)[:, :, :3]
        self.state = img_rgb
        return img_rgb

    def step(self, action):
        observation = self.observe()
        self.episode_length += 1

        if (action == DfActionSpace.up):
            self.client.moveByDistance( 0, 0, self.up_distance )
        elif (action == DfActionSpace.down):
            self.client.moveByDistance( 0, 0, -self.up_distance )
        elif (action == DfActionSpace.turn_right):
            self.client.turnByDegree( self.turn_degree )
            self.current_degree += self.turn_degree
            self.current_degree %= 360
        elif (action == DfActionSpace.turn_left):
            self.client.turnByDegree( -self.turn_degree )
            self.current_degree -= self.turn_degree
            self.current_degree %= 360
        self.client.moveByDistance( self.move_distance, 0, 0 )
        self.distance_moved += self.move_distance * np.cos(self.current_degree / 180 * np.pi)

        if self.distance_moved > self.max_distance:
            self.max_distance = self.distance_moved
       
        if self.max_distance > 7000:
            self.done = True
            # reward = self.max_distance / 100
            reward = 1
        elif self.client.isHit() or self.episode_length > 170:
            self.done = True
            # reward = self.max_distance / 100
            reward = -1
        else:
            reward = 0

        info = {'max_distance': self.max_distance / 100}

        return [observation, reward, self.done, info]
