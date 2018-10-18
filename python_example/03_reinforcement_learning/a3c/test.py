import time

import torch
import torch.nn.functional as F
from torch.autograd import Variable

from environment import create_env
from a3c.model import ActorCritic

def test(rank, args, shared_model, counter, lock):
    torch.manual_seed(args.seed + rank)

    env = create_env(rank)

    model = ActorCritic(env.observation_space.shape[0], env.action_space)

    model.eval()

    state = torch.from_numpy(env.reset())
    reward_sum = 0
    done = True

    start_time = time.time()

    episode_length = 0
    while True:
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
            print("Time {}, num steps {}, FPS {:.0f}, episode reward {}, episode length {}".format(
                time.strftime("%Hh %Mm %Ss",
                              time.gmtime(time.time() - start_time)),
                counter.value, counter.value / (time.time() - start_time),
                reward_sum, episode_length))
            reward_sum = 0
            episode_length = 0
            time.sleep(60)
