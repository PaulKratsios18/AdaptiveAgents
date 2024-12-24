import numpy as np
import random
import matplotlib.pyplot as plt

class GameEnv:
    def __init__(self):
        # place the car
        self.car_index = random.randint(0, 2)
    
    def open_door(self, initial_index, switch):
        if switch:
            return 0 if initial_index == self.car_index else 100
        else:
            return 100 if initial_index == self.car_index else 0

class Agent:
    def __init__(self, alpha):
        if alpha <= 0 or alpha > 1:
            raise ValueError('The learning rate should be between zero and one')
        self.alpha = alpha
        self.Q_table = np.zeros(2)
    
    def choose_initial_door(self):
        return random.randint(0, 2)
    
    def choose_if_switch(self):
        return np.argmax(self.Q_table)

    def update_Q_table(self, action, reward):
        old_q_value = self.Q_table[action]
        self.Q_table[action] = (1 - self.alpha) * old_q_value + self.alpha * reward

def evaluate_agent(alpha, episodes=1000):
    agent = Agent(alpha)
    win_counts = 0
    for _ in range(episodes):
        env = GameEnv()
        initial_door = agent.choose_initial_door()
        action = agent.choose_if_switch() if random.uniform(0, 1) > 0.2 else random.choice([0, 1])
        r = env.open_door(initial_door, action)
        agent.update_Q_table(action, r)
        if r == 100:
            win_counts += 1
    return win_counts / episodes

if __name__ == "__main__":
    alpha_values = np.linspace(0.01, 1, 20)  # Define the range of alpha values
    win_rates = []

    for alpha in alpha_values:
        win_rate = evaluate_agent(alpha)
        win_rates.append(win_rate)

    best_alpha = alpha_values[np.argmax(win_rates)]
    print("Best alpha:", best_alpha)

    # Plot the win rates over alpha values
    plt.figure(figsize=(10, 6))
    plt.plot(alpha_values, win_rates, marker='o')
    plt.xlabel('Alpha')
    plt.ylabel('Win Rate')
    plt.title('Win Rate of Q-Learning Agent for Different Alpha Values')
    plt.grid(True)
    plt.show()
