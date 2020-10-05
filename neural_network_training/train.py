from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2
import tensorflow as tf
import numpy as np
import stable_baselines
from gym import Env
from gym.spaces import Box


# Dummy environment just for creation of the model
class DummyEnv(Env):
    def __init__(self, input_size=8):

        # action is a single number as output of the NN
        self.action_space = Box(low=-1.0, high=+1.0,
                                shape=(1,), dtype=np.float32)
        # observation is a 2-dim vector as input (add more 1.0 for longer vector)
        obs = np.array([1.0 for _ in range(input_size)])
        self.observation_space = Box(low=-obs, high=obs, dtype=np.float32)


max_depth = 5
max_width_exponent = 10  # 2^10 = 1024
max_input_exponent = 7  # 2^7 = 128
act_function = tf.nn.relu

policy_width = 1
input_size = 1


for policy_depth in range(1, max_depth + 1):  # num
    while policy_width <= 2 ** max_width_exponent:
        while input_size <= 2 ** max_input_exponent:
            # network architecture
            policy_kwargs = {
                'act_fun': act_function,
                'layers': [policy_width for _ in range(policy_depth)]
            }

            env = DummyEnv()
            # env = make_vec_env('CartPole-v1', n_envs=2)

            model = PPO2(MlpPolicy, env, policy_kwargs=policy_kwargs)
            # model.learn(total_timesteps=25000)

            print('Model created with depth %d, width %d, and input size %d'
                  % (policy_depth, policy_width, input_size))
            file_name = "dummy_networks/ppo2_dummy_%d_%d_%d" % (
                policy_depth, policy_width, input_size)
            model.save(file_name)
            input_size *= 2

        input_size = 1
        policy_width *= 2

    policy_width = 1
