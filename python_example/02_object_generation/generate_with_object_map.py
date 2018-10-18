import sys
import time
import argparse

import numpy as np

sys.path.append('../')
from VividClient import *

parser = argparse.ArgumentParser(description='generate with object map')
parser.add_argument('--ip', default='127.0.0.1',
                    help='ip (default: 127.0.0.1)')
parser.add_argument('--port', type=int, default=16612,
                    help='port (default: 16612)')
parser.add_argument('--infile', default='input.txt',
                    help='input file name (default: input.txt)')
parser.add_argument('--item-type', type=int, default=-1,
                    help='item type (default: -1: fire)')

if __name__ == '__main__':

    args = parser.parse_args()
    client = VividClient(ip=args.ip, port=args.port)
    
    coor_list = []
    f = open(args.infile) 
    for coor in f:
        coor = coor[1:-3]
        c = coor.split(',')
        coor_list.append(c)
    f.close()
    
    coor_list = np.array(coor_list, dtype=float)
    
    for c in coor_list:
        client.createMapObject(args.item_type, c[0], c[1], c[2])
