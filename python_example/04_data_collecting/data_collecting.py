'''
An Example for collecting human action data by controlling a drone.
Test in the "Hospital" scene
'''

import math
import time
import datetime
import os
import sys
import argparse

sys.path.append('../')
from VividClient import *

parser = argparse.ArgumentParser(description='collecting human action data')
parser.add_argument('dirs',
                    help='output directory')
parser.add_argument('--ip', default='127.0.0.1',
                    help='ip (default: 127.0.0.1)')
parser.add_argument('--port', type=int, default=16612,
                    help='port (default: 16612)')
parser.add_argument('--item-type', type=int, default=-1,
                    help='item type (default: -1: fire)')

def image_capturing(requests, vivid_client, filedir):
    if not os.path.exists(filedir):
        os.makedirs(filedir)
        
    filename = datetime.datetime.now().strftime("%m%d-%H%M%S.%f")
    
    responses = vivid_client.simGetImages(requests)
    for i, response in enumerate(responses):
        VividClient.write_file(os.path.join(filedir, '{}_{}.png'.format(filename, i)), response.image_data_uint8)

def create_target(vivid_client, item_type, distance = 500):
    agent_pos = vivid_client.getLocation()
    target_pos = [agent_pos[0] + distance, agent_pos[1], agent_pos[2]]
    vivid_client.createMapObject(item_type, *target_pos)
    return agent_pos, target_pos

def move_around_xy(vivid_client, target_position, turn_degree):  
    ag_x, ag_y, ag_z = vivid_client.getLocation()
    obj_x, obj_y, obj_z = target_position
    radian = math.radians(turn_degree)
    sin = math.sin(radian)
    cos = math.cos(radian)

    x1 = ag_x - obj_x
    y1 = ag_y - obj_y
    x2 = x1 * cos - y1 * sin
    y2 = x1 * sin + y1 * cos
    ag_new_x, ag_new_y, ag_new_z = [x2 + obj_x, y2 + obj_y, ag_z]
    move_x, move_y, move_z = [ag_new_x - ag_x, ag_new_y - ag_y, ag_new_z - ag_z]

    vivid_client.moveByDistance(move_x, move_y, move_z)

if __name__ == '__main__':
    args = parser.parse_args()
    requests = [ImageRequest(0, AirSimImageType.Scene),
                ImageRequest(0, AirSimImageType.Segmentation)]

    rotate_degree = 45
    record_period = 5
    count = 360 / rotate_degree
    current_t = time.time()
    t_end = current_t + count*record_period
    t_record = current_t + record_period

    client = VividClient(ip=args.ip, port=args.port)
    #Test in the "Hospital" map
    client.setLocation(-181,-1000,187.5)
    #_, tar_pos = create_target(client, args.item_type)
    #Test in the "Hospital" map
    tar_pos = [303.71, -1000, 187.5]

    deg = 0
    while time.time() < t_end:
        
        while time.time() < t_record:
            image_capturing(requests, client, args.dirs)
        client.turnByDegree(-deg)
        move_around_xy(client, tar_pos, rotate_degree)
        
        deg = (deg + rotate_degree) % 360
        client.turnByDegree(deg)
        time.sleep(1)
        t_record = t_record + record_period
