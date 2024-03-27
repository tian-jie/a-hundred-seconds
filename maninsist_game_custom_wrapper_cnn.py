import math

import gym
import numpy as np

from game import ManInsistGame

class PlayEnv(gym.Env):
    def __init__(self, seed=0, board_size=(100, 100), silent_mode=True, limit_step=True):
        super().__init__()
        self.game = ManInsistGame(seed=seed, board_size = board_size, silentMode=silent_mode, enemyCount=2)
        self.game.reset()

        self.silent_mode = silent_mode

        # ??? 创建一个n维的离散空间 
        self.action_space = gym.spaces.Discrete(5) # 0: UP, 1: LEFT, 2: RIGHT, 3: DOWN
        
        self.observation_space = gym.spaces.Box(
            low=0, high=2,
            shape=(1, board_size[0]*7, board_size[1]*7),
            dtype=np.uint8
        )

    def reset(self):
        self.game.reset()

        obs = self._generate_observation()
        return obs
    
    def step(self, action):
        self.done = self.game.step(25, action) # info = {"snake_size": int, "snake_head_pos": np.array, "prev_snake_head_pos": np.array, "food_pos": np.array, "food_obtained": bool}
        obs = self._generate_observation()

        reward = 0.0
        if(self.game.status == "playing"):
            reward = self.game.gameDuration/1000
        elif(self.game.status == "gameover"):
            reward = 0

        return obs, reward, self.done, None
    
    def render(self):
        self.game.render()

    def get_action_mask(self):
        return np.array([[self._check_action_validity(a) for a in range(self.action_space.n)]])
    
    # Check if the action is against the current direction of the snake or is ending the game.
    def _check_action_validity(self, action):
        return True

    # EMPTY: BLACK; SnakeBODY: GRAY; SnakeHEAD: GREEN; FOOD: RED;
    def _generate_observation(self):
        obs = np.zeros((self.game.屏幕宽度, self.game.屏幕高度), dtype=np.uint8)
        # obs = np.zeros((1000, 1000), dtype=np.uint8)

        #obs = np.stack((obs), axis=-1)

        obs[tuple((self.game.player.posx, self.game.player.posy))] = 2
        for enemy in self.game.bullets:
            obs[tuple((enemy.posx, enemy.posy))] = 1

        
        # # Set the snake body to gray with linearly decreasing intensity from head to tail.
        # # 给蛇的身体从头到尾做梯队灰度
        # obs[tuple(np.transpose(self.game.snake))] = np.linspace(200, 50, len(self.game.snake), dtype=np.uint8)
        
        # # Stack single layer into 3-channel-image.
        # # 三色空间
        # obs = np.stack((obs, obs, obs), axis=-1)
        
        # # Set the snake head to green and the tail to blue
        # # 染色
        # obs[tuple(self.game.snake[0])] = [0, 255, 0]
        # obs[tuple(self.game.snake[-1])] = [255, 0, 0]

        # # Set the food to red
        # # 染色
        # obs[self.game.food] = [0, 0, 255]


        # Enlarge the observation to 84x84
        obs = np.repeat(np.repeat(obs, 7, axis=0), 7, axis=1)

        return obs

# Test the environment using random actions
# NUM_EPISODES = 100
# RENDER_DELAY = 0.001
# from matplotlib import pyplot as plt

# if __name__ == "__main__":
#     env = SnakeEnv(silent_mode=False)
    
    # # Test Init Efficiency
    # print(MODEL_PATH_S)
    # print(MODEL_PATH_L)
    # num_success = 0
    # for i in range(NUM_EPISODES):
    #     num_success += env.reset()
    # print(f"Success rate: {num_success/NUM_EPISODES}")

    # sum_reward = 0

    # # 0: UP, 1: LEFT, 2: RIGHT, 3: DOWN
    # action_list = [1, 1, 1, 0, 0, 0, 2, 2, 2, 3, 3, 3]
    
    # for _ in range(NUM_EPISODES):
    #     obs = env.reset()
    #     done = False
    #     i = 0
    #     while not done:
    #         plt.imshow(obs, interpolation='nearest')
    #         plt.show()
    #         action = env.action_space.sample()
    #         # action = action_list[i]
    #         i = (i + 1) % len(action_list)
    #         obs, reward, done, info = env.step(action)
    #         sum_reward += reward
    #         if np.absolute(reward) > 0.001:
    #             print(reward)
    #         env.render()
            
    #         time.sleep(RENDER_DELAY)
    #     # print(info["snake_length"])
    #     # print(info["food_pos"])
    #     # print(obs)
    #     print("sum_reward: %f" % sum_reward)
    #     print("episode done")
    #     # time.sleep(100)
    
    # env.close()
    # print("Average episode reward for random strategy: {}".format(sum_reward/NUM_EPISODES))
