import argparse

import torch
import torch.nn.functional as F
from torch.autograd import Variable

from a3c.envs import create_unreal_env
from a3c.model import ActorCritic
from pspnet.utils import color_class_image

import numpy as np
import imageio

parser = argparse.ArgumentParser(description='dragonfly A3C agent')
parser.add_argument('--start-id', type=int, default=0,
                    help='environment start id (default: 0)')
parser.add_argument('checkpoint', type=str,
                    help='path to the model checkpoint')

if __name__ == '__main__':
    args = parser.parse_args()

    env = create_unreal_env(args.start_id)
    model = ActorCritic(env.observation_space.shape[0], env.action_space)
    model.eval()
    model.load_state_dict(torch.load(args.checkpoint))

    cx = Variable(torch.zeros(1, 256), volatile=True)
    hx = Variable(torch.zeros(1, 256), volatile=True)

    episode_length = 0
    done = False

    state = env.reset()
    segmented_image = color_class_image(np.argmax(state.transpose(1, 2, 0), axis=2))
    segmented = [segmented_image]
    original = [env.render()]

    while not done:
        episode_length += 1
        cx = Variable(cx.data, volatile=True)
        hx = Variable(hx.data, volatile=True)

        value, logit, (hx, cx) = model((Variable(
            torch.from_numpy(state).unsqueeze(0), volatile=True), (hx, cx)))
        prob = F.softmax(logit, dim=1)
        action = prob.max(1, keepdim=True)[1].data.numpy()

        state, reward, done, info = env.step(action[0, 0])
        
        segmented_image = color_class_image(np.argmax(state.transpose(1, 2, 0), axis=2))
        segmented.append(segmented_image)
        original.append(env.render())

    print('episode reward: {}, episode length: {}, distance moved: {:3.2f} m'.\
          format(reward, episode_length, info['max_distance']))
    imageio.mimwrite('segmented.gif', segmented + segmented[-1:] * 20)
    imageio.mimwrite('original.gif', original + original[-1:] * 20)
