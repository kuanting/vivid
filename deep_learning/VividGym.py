# Implement OpenAI Gym interface
import gym
from gym import spaces
from VividClient import *

class DfActionSpace:
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
    # This is the safe distance before hitting a obstacle
    move_distance = 60 	# cm
    up_distance = 40 	# cm
    turn_degree = 30 	# degree
    screen_width = 256
    screen_height = 144
    done = False

    def __init__(self, ip='127.0.0.1', port=16612):
        self.action_space = gym.spaces.Discrete(8) 
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(self.screen_width*self.screen_height*3,));
        # Connect to Vivid mode
        self.client = VividClient(ip=ip, port=port)

    def reset(self):
        self.client.reset() 
        self.done = False
        return self.observe()

    def render(self):
        pass

    def observe(self):
        # Get uncompressed screenshot from Camera 0
        resp = self.client.simGetImages([ImageRequest(0, AirSimImageType.Scene, False, False)])
        # Remove Alpha
        img_rgba = resp[0].image_data_uint8
        img_rgb = bytearray(self.screen_width*self.screen_height*3)
        j = 0
        for i in range(self.screen_width*self.screen_height*4):
            if (i % 4 == 3):
                continue 
            else:
                img_rgb[j] = img_rgba[i]
                j = j + 1

        return img_rgb


    def step(self, action):
        # Get screenshot
        observation = self.observe()

        if (action == DfActionSpace.forward):
            self.client.moveByDistance( self.move_distance, 0, 0 );
        elif (action == DfActionSpace.backward):
            self.client.moveByDistance( -self.move_distance, 0, 0 );
        elif (action == DfActionSpace.right):
            self.client.moveByDistance( 0, self.move_distance, 0 );
        elif (action == DfActionSpace.left):
            self.client.moveByDistance( 0, -self.move_distance, 0 );
        elif (action == DfActionSpace.up):
            self.client.moveByDistance( 0, 0, self.up_distance );
        elif (action == DfActionSpace.down):
            self.client.moveByDistance( 0, 0, -self.up_distance );
        elif (action == DfActionSpace.turn_right):
           self.client.turnByDegree( self.turn_degree );
        elif (action == DfActionSpace.turn_left):
           self.client.turnByDegree( -self.turn_degree );
       
        self.done = self.client.isHit();

        if (self.done == True):
            reward = -1;
        else:
            if (action < 4): # Only xy-moves have scores
                reward = 1;
            else:
                reward = 0;

        info = ""

        return [observation, reward, self.done, info];
            
