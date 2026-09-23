
from pathlib import Path

from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.callbacks import MaskableEvalCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor

from tetris_rl.tetris_env import TetrisENV
from tetris_rl.tetris_env_movement import TetrisENVMov


check_env(TetrisENV())

train_env = Monitor(TetrisENV(), info_keywords=("points", "lines", "pieces_locked"))
eval_env = Monitor(TetrisENV(), info_keywords=("points", "lines", "pieces_locked"))

callback = MaskableEvalCallback(
    eval_env,
    best_model_save_path="models/best",
    log_path="models/evaluations",
    eval_freq=20_000,
    n_eval_episodes=20,
    deterministic=True,
)

model = MaskablePPO(
    "MultiInputPolicy",
    train_env,
    learning_rate=3e-4,
    gamma=0.99,
    verbose=1,
    device="auto",
    seed=42,
    tensorboard_log="logs",
)

model.learn(total_timesteps=10_000, callback=callback, device="cuda")

Path("models").mkdir(exist_ok=True)
model.save("models/tetris_maskable_ppo")
train_env.close()
eval_env.close()