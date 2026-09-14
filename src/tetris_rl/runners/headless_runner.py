from tetris_rl.tetris_env import TetrisENV
from stable_baselines3 import DQN


def run(game):
    env = TetrisENV()
    model = DQN.load("tetris_dqn", device="cpu")

    obs, info = env.reset()

    total_reward = 0

    while True:
        
        action, _ = model.predict(obs, deterministic=True)
        print(env.actions[int(action)].name)

        obs, reward, terminated, truncated, info = env.step(int(action))

        assert env.observation_space.contains(obs)
        total_reward += reward

        if terminated or truncated:
            break

    print("Pasos:", env.steps)
    print("Líneas:", env.game.lines_cleared)
    print("Recompensa:", total_reward)
    print("Game over:", terminated)
    print("Límite de pasos:", truncated)

    env.close()