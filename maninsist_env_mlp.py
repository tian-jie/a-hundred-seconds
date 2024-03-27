import random
import numpy as np
import torch.nn as nn 
import torch

from game import ManInsistGame

class Environment:
    def __init__(self):
        self.board_size = 600
        seed = random.randint(0, 1e9)
        self.game = ManInsistGame(enemyCount=99, board_size=(self.board_size, self.board_size), silentMode=True, seed=seed)

    def reset(self):
        self.game.reset()
        self.red_dot = np.array((int(self.game.player.posx), int(self.game.player.posy)))
        self.white_dots = np.array([[]])
        for white in self.game.bullets:
            self.white_dots = np.append(self.white_dots, [int(white.posx), int(white.posy)])

        
    def step(self, action):
        done, info = self.game.step(50, action)
        self.red_dot = np.array((int(self.game.player.posx), int(self.game.player.posy)))
        self.white_dots = np.array([[]])
        for white in self.game.bullets:
            self.white_dots = np.append(self.white_dots, [int(white.posx), int(white.posy)])

        # 计算奖励
        reward = 0
        for white_dot in self.white_dots:
            distance = np.linalg.norm(self.red_dot-white_dot) - 5
            sign = 1
            if distance<0:
                sign = -1
            reward = distance * distance / 1000 * sign
        
        if done:
            reward = -100

        info = {
            "red_dot": self.red_dot,
            "white_dots": self.white_dots
        }
        return reward, done, info
    

class Agent:
    def __init__(self):
        # 初始化MLP
        self.mlp = MLP(32, 100, 2, 5, 0.5)
    
    def act(self, state):
        # 根据状态预测动作
        action = self.mlp.(state)
        return action




# class MLP(nn.Module):
#     def __init__(self, user_num, item_num, factor_num, num_layers, dropout):
#         super(MLP, self).__init__()

#         self.embed_user_MLP = nn.Embedding(user_num, factor_num * (2 ** (num_layers - 1)))
#         self.embed_item_MLP = nn.Embedding(item_num, factor_num * (2 ** (num_layers - 1)))

#         MLP_modules = []
#         for i in range(num_layers):
#             input_size = factor_num * (2 ** (num_layers - i))
#             MLP_modules.append(nn.Dropout(p=dropout))
#             MLP_modules.append(nn.Linear(input_size, input_size // 2))
#             MLP_modules.append(nn.ReLU())
#         self.MLP_layers = nn.Sequential(*MLP_modules)

#         self.predict_layer = nn.Linear(factor_num, 1)

#         self._init_weight_()

#     def _init_weight_(self):
#         nn.init.normal_(self.embed_user_MLP.weight, std=0.01)
#         nn.init.normal_(self.embed_item_MLP.weight, std=0.01)

#         for m in self.MLP_layers:
#             if isinstance(m, nn.Linear):
#                 nn.init.xavier_uniform_(m.weight)
#                 nn.init.kaiming_uniform_(self.predict_layer.weight, a=1, nonlinearity='sigmoid')

#     def forward(self, user, item):
#         embed_user_MLP = self.embed_user_MLP(user)
#         embed_item_MLP = self.embed_item_MLP(item)
#         interaction = torch.cat((embed_user_MLP, embed_item_MLP), -1)
#         output_MLP = self.MLP_layers(interaction)
#         prediction = self.predict_layer(output_MLP)
#         return prediction.view(-1)

# # 定义奖励函数
# def reward_function(state, action):
#     reward = 0
#     # 计算奖励
#     for white_dot in state["white_dots"]:
#         if np.linalg.norm(state["erd_dot"] - white_dot) < 1:
#             reward = -1
#             break
#     return reward

# 定义强化算法
def train(env: Environment, agent: Agent):
    # 训练agent
    for episode in range(1000):
        state = env.reset()
        done = False
        while not done:
            action = agent.act(state)
            reward, done, state = env.step(50, action)

            # 更新MLP参数
            agent.mlp.update(state, action, reward)

# 训练程序
env = Environment()
agent =Agent()
train(env, agent)