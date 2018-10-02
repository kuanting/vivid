from collections import deque
import os
from datetime import datetime
import time
import msgpackrpc

import torch
import torch.nn.functional as F
from torch.autograd import Variable

from a3c.envs import create_unreal_env
from a3c.model import ActorCritic
from tensorboardX import SummaryWriter

class CheckpointSaver():
    def __init__(self, root_path):
        if not os.path.isdir(root_path):
            os.makedirs(root_path)
        self.root_path = root_path

    def save(self, step, state_dict):
        torch.save(state_dict,
                   os.path.join(self.root_path,
                                'step{}'.format(step)))
        print('checkpoint saved at step {}'.format(step))

def test(rank, args, shared_model, counter, lock):
    torch.manual_seed(args.seed + rank)

    env = create_unreal_env(rank, segmentation=not args.no_segmentation)

    model = ActorCritic(env.observation_space.shape[0], env.action_space)

    model.eval()

    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    run_id = current_time + '_noseg' if args.no_segmentation else current_time
    writer = SummaryWriter(os.path.join('runs', run_id))
    checkpoint_saver = CheckpointSaver(os.path.join('checkpoints', run_id))
    episode = 0
    state = torch.from_numpy(env.reset())
    reward_sum = 0
    done = True

    start_time = time.time()

    episode_length = 0
    while True:
        try:
            episode_length += 1
            # Sync with the shared model
            if done:
                state = torch.from_numpy(env.reset())
                model.load_state_dict(shared_model.state_dict())
                cx = Variable(torch.zeros(1, 256), volatile=True)
                hx = Variable(torch.zeros(1, 256), volatile=True)
            else:
                cx = Variable(cx.data, volatile=True)
                hx = Variable(hx.data, volatile=True)

            value, logit, (hx, cx) = model((Variable(
                state.unsqueeze(0), volatile=True), (hx, cx)))
            prob = F.softmax(logit, dim=1)
            action = prob.max(1, keepdim=True)[1].data.numpy()

            state, reward, done, info = env.step(action[0, 0])
            state = torch.from_numpy(state)
            reward_sum += reward

            if done:
                episode += 1
                print("Time {}, num steps {}, FPS {:.0f}, episode reward {}, episode length {}".format(
                    time.strftime("%Hh %Mm %Ss",
                                  time.gmtime(time.time() - start_time)),
                    counter.value, counter.value / (time.time() - start_time),
                    reward_sum, episode_length))
                writer.add_scalar('episode_reward', reward_sum, counter.value)
                writer.add_scalar('max_distance', info['max_distance'], counter.value)
                if episode % 10 == 0:
                    checkpoint_saver.save(counter.value,
                                          shared_model.state_dict())
                reward_sum = 0
                episode_length = 0
                time.sleep(60)

        except msgpackrpc.error.TimeoutError:
            print('Environment {} crashed, restoring...'.format(rank))
            reward_sum = 0
            episode_length = 0
            env.reconnect()
            done = True
            print('Environment {} restored'.format(rank))
