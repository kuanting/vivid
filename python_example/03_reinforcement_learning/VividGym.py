# Implement OpenAI Gym interface
import gym
import numpy as np
from gym import spaces
import json
import time
import sys

sys.path.append('../')
from VividClient import *
import utils

class DroneActionSpace:
    forward = 0
    backward = 1
    right = 2 
    left = 3 
    up = 4 
    down = 5
    turn_right = 6
    turn_left = 7
   

class VividEnv(gym.Env):

    # Define moving distance or turning degree
    # This is the safe distance before hitting an obstacle
    move_distance = 60  # cm
    up_distance = 40    # cm
    turn_degree = 30    # degree
    screen_width = 256
    screen_height = 144

    def __init__(self, ip, port, map_id, spawn_points_file):
        self.action_space = gym.spaces.Discrete(8) 
        self.observation_space = gym.spaces.Box(
            low=0, high=255,
            shape=(self.screen_height, self.screen_width, 3),
            dtype=np.float32);
        
        self.map_id = map_id

        # Connect to Vivid mode
        self.client = VividClient(ip=ip, port=port)

        # initialize environment settings
        self.done = False
        self.spawn_points = utils.load_spawn_points(spawn_points_file)
        self.spawn_points = np.random.permutation(self.spawn_points)
        # use the first coordination as goal object
        self.client.createMapObject(VividMapObjectType.Chair,
                                    *self.spawn_points[0])

    def reset(self):
        # randomly choose a spawn point
        pos = self.spawn_points[ np.random.randint(1, len(self.spawn_points)) ]
        self.client.setLocation(*pos)
        # offset on z-axis and yaw angle
        self.client.moveByDistance(0, 0, np.random.randint(0, 150))
        self.client.turnByDegree(np.random.randint(0, 360))

        self.done = False
        self.episode_length = 0
        return self.observe()

    def observe(self):
        # Get uncompressed screenshot from Camera 0
        resp = self.client.simGetImages([ImageRequest(0, AirSimImageType.Scene, False, False)])
        img_rgb = np.array(bytearray(resp[0].image_data_uint8))\
            .reshape(self.screen_height, self.screen_width, 4)[:, :, :3] # Remove alpha
        return img_rgb

    def close(self):
        self.client.client.close()

    def step(self, action):
        # Get screenshot
        observation = self.observe()

        if (action == DroneActionSpace.forward):
            self.client.moveByDistance( self.move_distance, 0, 0 );
        elif (action == DroneActionSpace.backward):
            self.client.moveByDistance( -self.move_distance, 0, 0 );
        elif (action == DroneActionSpace.right):
            self.client.moveByDistance( 0, self.move_distance, 0 );
        elif (action == DroneActionSpace.left):
            self.client.moveByDistance( 0, -self.move_distance, 0 );
        elif (action == DroneActionSpace.up):
            self.client.moveByDistance( 0, 0, self.up_distance );
        elif (action == DroneActionSpace.down):
            self.client.moveByDistance( 0, 0, -self.up_distance );
        elif (action == DroneActionSpace.turn_right):
           self.client.turnByDegree( self.turn_degree );
        elif (action == DroneActionSpace.turn_left):
           self.client.turnByDegree( -self.turn_degree );
       
        self.episode_length += 1
        self.done = self.client.isHit() or self.episode_length > 300;

        if self.done:
            collision_info = self.client.getCollisionInfo()
            # The object created by API always has object_id = -1
            if collision_info.object_id == -1:
                # hitting the goal
                reward = 100
            else:
                # hitting the obstacle
                reward = -1
        else:
            reward = 0

        info = ''

        return observation, reward, self.done, info;
