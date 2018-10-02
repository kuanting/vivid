import argparse
import os

import torch
import torch.multiprocessing as mp

import a3c.my_optim as my_optim
from a3c.envs import create_unreal_env
from a3c.model import ActorCritic
from a3c.test import test
from a3c.train import train

# Based on
# https://github.com/pytorch/examples/tree/master/mnist_hogwild
# Training settings
parser = argparse.ArgumentParser(description='A3C')
parser.add_argument('--lr', type=float, default=0.0001,
                    help='learning rate (default: 0.0001)')
parser.add_argument('--gamma', type=float, default=0.99,
                    help='discount factor for rewards (default: 0.99)')
parser.add_argument('--tau', type=float, default=1.00,
                    help='parameter for GAE (default: 1.00)')
parser.add_argument('--entropy-coef', type=float, default=0.01,
                    help='entropy term coefficient (default: 0.01)')
parser.add_argument('--value-loss-coef', type=float, default=0.5,
                    help='value loss coefficient (default: 0.5)')
parser.add_argument('--max-grad-norm', type=float, default=50,
                    help='value loss coefficient (default: 50)')
parser.add_argument('--seed', type=int, default=1,
                    help='random seed (default: 1)')
parser.add_argument('--num-processes', type=int, default=4,
                    help='how many training processes to use (default: 4)')
parser.add_argument('--num-steps', type=int, default=20,
                    help='number of forward steps in A3C (default: 20)')
parser.add_argument('--no-shared', default=False,
                    help='use an optimizer without shared momentum.')
parser.add_argument('--no-segmentation', action='store_true',
                    help='train in environments without segmentation.')
parser.add_argument('--start-id', type=int, default=0,
                    help='environment start id (default: 0)')


if __name__ == '__main__':
    args = parser.parse_args()
    mp.set_start_method('spawn', force=True)

    torch.manual_seed(args.seed)
    env = create_unreal_env(0, segmentation=not args.no_segmentation, fake=True)
    shared_model = ActorCritic(
        env.observation_space.shape[0], env.action_space)
    shared_model.share_memory()

    if args.no_shared:
        optimizer = None
    else:
        optimizer = my_optim.SharedAdam(shared_model.parameters(), lr=args.lr)
        optimizer.share_memory()

    processes = []

    counter = mp.Value('i', 0)
    lock = mp.Lock()

    p = mp.Process(target=test, args=(args.start_id + args.num_processes,
                                      args, shared_model, counter, lock))
    p.start()
    processes.append(p)

    for rank in range(0, args.num_processes):
        p = mp.Process(target=train, args=(args.start_id + rank, 
                                           args, shared_model, counter, lock, optimizer))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
