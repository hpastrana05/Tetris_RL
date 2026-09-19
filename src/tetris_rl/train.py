

from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor

from tetris_rl.tetris_env import TetrisENV
from tetris_rl.tetris_env_movement import TetrisENVMov

env = TetrisENVMov()


# Checks compatibility with library 
check_env(env)

# Monitors the duration and rewards of steps
env = Monitor(env)

model = DQN(
    "MultiInputPolicy",
    env,
    buffer_size = 100_000,
    learning_starts = 10_000,
    exploration_fraction = 0.05,
    verbose = 1,
    device="cuda" # "cuda" for gpu
)

model.learn(total_timesteps=500_000)
model.save("tetris_dqn_move")

env.close()