import numpy as np
from collections import deque

# 创建经验回放缓冲区
memory = deque(maxlan=2000)

# 探索率
epsilon = 1.0
epsilon_min = 0.01
epsilon_decay = 0.995

def act(state):
    if np.random.rand() <= epsilon:
        return env.action_sample.sample()
    else:
        return np.argmax(model.predict(state))


