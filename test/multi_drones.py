import time
import math
from VividClient import *

client = VividClient(ip="192.168.0.13");

client.client.call('spawnPawn', 0, 'drone1', 0, 0, 500)
time.sleep(0.5)
client.client.call('spawnPawn', 0, 'drone2', -200, 0, 500)
time.sleep(0.5)
client.client.call('spawnPawn', 0, 'drone3', 0, -200, 300)
time.sleep(0.5)
client.client.call('spawnPawn', 0, 'drone4', 200, 0, 500)
time.sleep(0.5)
client.client.call('spawnPawn', 0, 'drone5', 0, 200, 500)
time.sleep(0.5)

turn_speed = 10 
turn_rad = math.radians(turn_speed) 
r = 200
start_x = 0
start_y = r 
while(True):
    for i in range(0, 9):
        x = r*math.cos(i*turn_rad) 
        y = r*math.sin(i*turn_rad) 

        dx = x - start_x
        dy = y - start_y
        start_x = x
        start_y = y 
        #print("x=", x, "\ty=", y)
        client.client.call('moveByDistance', 3, dx, dy, 0) 



