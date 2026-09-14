

from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor

from tetris_rl.tetris_env import TetrisENV

env = TetrisENV()

# Checks compatibility with library 
check_env(env)

# Monitors the duration and rewards of steps
env = Monitor(env)

model = DQN(
    "MultiInputPolicy",
    env,
    buffer_size = 50_000,
    learning_starts = 5_000,
    exploration_fraction = 0.3,
    verbose = 1,
    device="cuda" # "cuda" for gpu
)

model.learn(total_timesteps=100_000)
model.save("tetris_dqn")

env.close()