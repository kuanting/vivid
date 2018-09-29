import os
import sys
import argparse

from os.path import join, exists
sys.path.append('../')
from VividClient import *
sys.path.append('02_object_generation/')

parser = argparse.ArgumentParser(description='get location')
parser.add_argument('--ip', default='127.0.0.1',
                    help='ip (default: 127.0.0.1)')
parser.add_argument('--port', type=int, default=16612,
                    help='port (default: 16612)')
parser.add_argument('--outfile', default='output.txt',
                    help='output file name (default: output.txt)')

if __name__ == '__main__':

    args = parser.parse_args()
    client = VividClient(ip=args.ip, port=args.port)

    while True:

        time.sleep(1)

        command = input()
        if command == 'g':
            with open(args.outfile, 'a') as texts:
                location = client.getLocation()
                print(location, file=texts)
        
        elif command == 'exit':
            print('Exit getPos')
            break
        
        else:
            print(command)
