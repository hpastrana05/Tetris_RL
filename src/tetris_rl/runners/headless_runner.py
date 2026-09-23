from tetris_rl.tetris_env import TetrisENV
from tetris_rl.tetris_env_movement import TetrisENVMov
from stable_baselines3 import DQN
import numpy as np

from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.utils import get_action_masks

model_path = "models/tetris_maskable_ppo"
ENV = TetrisENV()

def run(game):
    env = ENV
    model = MaskablePPO.load(model_path, device="auto")

    obs, info = env.reset()
    total_reward = 0

    while True:
        action_masks = env.action_masks()

        action, _ = model.predict(
            obs,
            deterministic=True,
            action_masks=action_masks,
        )

        obs, reward, terminated, truncated, info = env.step(int(action))
        total_reward += reward

        if terminated or truncated:
            break

    print("Puntos:", info["points"])
    print("Piezas:", info["pieces_locked"])
    print("Líneas:", info["lines"])
    print("Recompensa:", total_reward)
    print("Game over:", terminated)
    print("Límite de pasos:", truncated)

    env.close()
