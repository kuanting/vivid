from VividClient import *
import random
import time

speed = 50
turnSpeed = 5 
client = VividClient(ip="127.0.0.1", port=16612);

while True:
    client.moveByDistance(speed, 0, 0);
    collision = client.isHit();
    if collision == True:
        # collision! Change direction randomly from degree -270, -180, -90, 90, 180, 270
        rand_degree = (round(random.random()*10) % 7 - 3)*90;

        print("Collision! Turn randomly by degree " + str(rand_degree));
        
        # Turn smoothly at turnSpeed
        deg = 0
        while deg < abs(rand_degree):
            if rand_degree > 0:
                client.turnByDegree(turnSpeed);
            else:
                client.turnByDegree(-turnSpeed);
            deg = deg + turnSpeed;
