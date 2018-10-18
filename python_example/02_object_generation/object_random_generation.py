import os
import sys
import time
import argparse

from os.path import join, exists
sys.path.append('../')
from VividClient import *
sys.path.append('02_object_generation/')

parser = argparse.ArgumentParser(description='object random generation')
parser.add_argument('--ip', default='127.0.0.1',
                    help='ip (default: 127.0.0.1)')
parser.add_argument('--port', type=int, default=16612,
                    help='port (default: 16612)')
parser.add_argument('--infile', default='object_map/small_office.txt',
                    help='input file name (default: object_map/small_office.txt)')
parser.add_argument('--item-type', type=int, default=0,
                    help='item type (default: 0: chair)')
parser.add_argument('--episode', type=int, default=5,
                    help='number of episodes')
parser.add_argument('--env', type=int, default=0,
                    help='the id of environment (default: 0: Small Office)')


def get_map_coor(filename):
    coor_list = []
    f = open(filename) 
    for coor in f:
        coor = coor[1:-3]
        c = coor.split(',')
        coor_list.append(c)
    f.close()
    coor_list = np.array(coor_list, dtype=float)

    return coor_list


def check_if_spot(cli_coor, cli_ang,obj_coor):
    '''
    input:
        cli_coor: 1-D array <np.ndarray> or list (3)
                  (x, y, z)
        cli_angl: scalar <float>
                  yaw degree
        obj_coor: 1-D array <np.ndarray> ot list (3)
                  (x, y, z)
    return:
        spotted : boolean
    '''
    dx = obj_coor[0] - cli_coor[0]
    dy = obj_coor[1] - cli_coor[1]
    dz = obj_coor[2] - cli_coor[2]
    r = np.sqrt(dx**2+dy**2)

    if np.abs(dz)<100 and r<150:
        radian = np.arctan2(dy, dx)
        degree = np.degrees(radian) - cli_angl
        #print(degree, cli_angl, np.degrees(radian))
        if degree >=0 and degree <=45:
            spotted=True
        elif degree >= -45 and degree<=0:
            spotted=True
        else:
            spotted=False
    else:
        spotted=False
    return spotted



if __name__=='__main__':
    args = parser.parse_args()
    client = VividClient(ip=args.ip, port=args.port)
    client.loadMap(map_id=args.env)

    coor_list = get_map_coor(args.infile)
    idx_c = np.random.choice(len(coor_list))
    c = coor_list[idx_c]

    client.createMapObject(args.item_type, c[0], c[1], c[2])
    
    e = 0
    while e < args.episode:
        cli_coor = client.getLocation()
        cli_angl = client.getRotation()[1]#yaw
        done = check_if_spot(cli_coor, cli_angl, c)

        if done:
            e+=1
            client.loadMap(map_id=args.env)

            idx_c = np.random.choice(len(coor_list))
            c = coor_list[idx_c]
            client.createMapObject(args.item_type, c[0], c[1], c[2])
