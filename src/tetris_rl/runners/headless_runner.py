from tetris_rl.tetris_env import TetrisENV
from tetris_rl.tetris_env_movement import TetrisENVMov
from stable_baselines3 import DQN

model_path = "models/tetris_dqn_piece_placement"
ENV = TetrisENV()

def run(game):
    env = ENV
    model = DQN.load(model_path, device="cuda")

    obs, info = env.reset()

    total_reward = 0

    while True:
        
        action, _ = model.predict(obs, deterministic=True)
        # print(env.actions[int(action)].name)

        obs, reward, terminated, truncated, info = env.step(int(action))

        assert env.observation_space.contains(obs)
        total_reward += reward

        if terminated or truncated:
            break

    print("Puntos:", env.game.points)
    print("Pasos:", env.steps)
    print("Líneas:", env.game.lines_cleared)
    print("Recompensa:", total_reward)
    print("Game over:", terminated)
    print("Límite de pasos:", truncated)

    env.close()
