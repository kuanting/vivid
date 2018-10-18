import sys
import random
import time

sys.path.append('../')
from VividClient import *

speed = 50
turnSpeed = 5 

# Connect to a VIVID environment through TCP/IP
client = VividClient(ip="127.0.0.1", port=16612);

while True:
    # Move forward
    client.moveByDistance(speed, 0, 0);

    # Check if we hit an obstacle
    collision = client.isHit();
    if collision == True:
        # Collision! Change direction randomly from degree -270, -180, -90, 90, 180, 270
        rand_degree = (round(random.random()*10) % 7 - 3)*90;

        print("Collision! Turn randomly by degree " + str(rand_degree));
        
        # Turn smoothly at turnSpeed for visual effect 
        # This part can be replaced by simply calling client.turnByDegree(rand_degree)
        deg = 0
        while deg < abs(rand_degree):
            if rand_degree > 0:
                client.turnByDegree(turnSpeed);
            else:
                client.turnByDegree(-turnSpeed);
            deg = deg + turnSpeed;
