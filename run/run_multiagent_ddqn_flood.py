#!/usr/bin/env python3

import sys, os

sys.path.append(os.getcwd())
print(os.getcwd())

for root, folders, files in os.walk(os.getcwd()):
    if ('\.' in root):
        continue
    for f in folders:
        if (f[0] == '.' or f[:2] == '__'):
            continue
        s = os.path.join(root, f)
        print(s)
        sys.path.append(s)

from algorithms.ma_ddqn import DDQN
from policies.deepq_state_plus_image_policy import StatePlusImagePolicy
from environments.envs.point_envs.surveillance import SurveillanceEnv
from surveillance_callback import callback
from run.util import train

def main():
    log_dir = '../../drl_for_surveillance_runs/flood/indiv/dqn/'

    env = SurveillanceEnv(nr_agents=2,
                          obs_mode='normal',
                          obs_type='flood',
                          obs_radius=500,
                          world_size=1000,
                          grid_size=100,
                          range_cutpoints=30,
                          angular_cutpoints=40,
                          torus=False,
                          dynamics='aircraft',
                          shared_reward=False,
                          render_dir=log_dir + 'video/')

    policy = StatePlusImagePolicy

    model = DQN(policy, env, prioritized_replay=False,
                verbose=1,
                tensorboard_log=log_dir,
                batch_size=2000,
                target_network_update_freq=1000,
                learning_starts=2000,
                train_freq=100,
                buffer_size=100000,
                exploration_fraction=0.7,
                exploration_final_eps=0.1,
                checkpoint_path=log_dir + 'models/',
                checkpoint_freq=10000)

    train(model, callback, num_timesteps=int(3e6), log_dir=log_dir)


if __name__ == '__main__':
    main()
