import math
import time # For debugging.

from game import ManInsistGame
import gym
import numpy as np

class PlayEnv(gym.Env):
    def __init__(self, seed=0, board_size=(300, 300), silent_mode=True, limit_step=True):
        super().__init__()
        self.game = ManInsistGame(seed=seed, board_size = board_size, silentMode=silent_mode, enemyCount=30)
        self.game.reset()

        self.action_space = gym.spaces.Discrete(5) # 0: UP, 1: LEFT, 2: RIGHT, 3: DOWN
        
        self.observation_space = gym.spaces.Box(
            low=0, high=2,
            shape=(board_size[0], board_size[1]),
            dtype=np.uint8
        ) # 0: empty, 1: player, -1: enemy(bullet)

        self.done = False

        self.reward_step_counter = 0

    def reset(self):
        self.game.reset()

        self.done = False
        self.reward_step_counter = 0

        obs = self._generate_observation()
        return obs
    
    def step(self, action):
        info = self.game.step(100, action=action) # info = {"snake_size": int, "snake_head_pos": np.array, "prev_snake_head_pos": np.array, "food_pos": np.array, "food_obtained": bool}
        obs = self._generate_observation()

        reward = 0.0
        self.reward_step_counter += 1

        red_dot = np.array((int(self.game.player.posx), int(self.game.player.posy)))
        white_dots = np.array([[]])
        for white in self.game.bullets:
            white_dots = np.append(white_dots, [int(white.posx), int(white.posy)])

        # 计算奖励，距离最近的一个白点的距离，越远越好
        minDistance = 1e9
        nearest_white_dot = white_dots[0]
        for white_dot in white_dots:
            distance = np.linalg.norm(red_dot-white_dot)
            if(distance<minDistance):
                minDistance = distance
                nearest_white_dot = white_dot

        if(minDistance<2):
            reward = -1000000 / self.reward_step_counter
            self.done = True
        else:
            reward = ((minDistance-2)/3)*((minDistance-2)/3)-1

        info = {
            "reward_step_counter": self.reward_step_counter,
            "nearest_white_dot": nearest_white_dot,
            "nearest_white_dot_distance": minDistance,
            "red_dot": red_dot
        }

        # print("step counter: " + str(self.reward_step_counter))
        # max_score: 144e - 1 = 390
        # min_score: -141 

        # Linear:
        # max_score: 288
        # min_score: -141

        return obs, reward, self.done, info
    
    def render(self):
        self.game.render()

    def get_action_mask(self):
        return np.array([[self._check_action_validity(a) for a in range(self.action_space.n)]])
    
    # Check if the action is against the current direction of the snake or is ending the game.
    def _check_action_validity(self, action):
        return True

    # EMPTY: 0; SnakeBODY: 0.5; SnakeHEAD: 1; FOOD: -1;
    def _generate_observation(self):
        obs = np.zeros((self.game.屏幕宽度, self.game.屏幕高度), dtype=np.uint8)
        obs[tuple((int(self.game.player.posx)-1, int(self.game.player.posy)-1))] = 2
        for enemy in self.game.bullets:
            obs[tuple((int(enemy.posx)-1, int(enemy.posy)-1))] = 1
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
