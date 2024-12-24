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
    # learning rate
    alpha = 0.1

    def __init__(self):
        # there is only one state, so the table is one dimensional
        # 0 = don't switch, 1 = switch
        self.Q_table = np.zeros(2)
    
    def choose_initial_door(self):
        return random.randint(0, 2)
    
    def choose_if_switch(self):
        return np.argmax(self.Q_table)

    def update_Q_table(self, action, reward):
        old_q_value = self.Q_table[action]
        # there is only one state, so no need to consider the future states
        self.Q_table[action] = (1 - self.alpha) * old_q_value + self.alpha * reward

class MontyAgent:
    def __init__(self):
        # Initialize Q-table for Monty
        self.Q_table = np.zeros(3)  # Monty has to choose which door to open

    def choose_door_to_open(self, initial_index, car_index):
        # Monty chooses the door to open based on Q-values
        options = [door for door in range(3) if door != initial_index and door != car_index]
        return np.argmax(self.Q_table[options])

    def update_Q_table(self, action, reward):
        # Update Monty's Q-table based on the received reward
        self.Q_table[action] += reward

if __name__ == "__main__":
    episodes = 100000
    agent = Agent()
    monty_agent = MontyAgent()
    win_counts = 0
    win_rates = []

    threshold = 0.2
    for e in range(episodes):
        env = GameEnv()
        if e % 100 == 0:
            threshold /= 2
        initial_door = agent.choose_initial_door()
        monty_choice = monty_agent.choose_door_to_open(initial_door, env.car_index)
        action = agent.choose_if_switch() if random.uniform(0, 1) > threshold else random.choice([0, 1])
        reward = env.open_door(initial_door, action)
        agent.update_Q_table(action, reward)
        monty_agent.update_Q_table(monty_choice, reward)
        if reward == 100:
            win_counts += 1
        win_rates.append(win_counts / (e + 1))

    print('Win rate:', win_rates[-1])

    plt.figure(figsize=(10, 6))
    plt.plot(win_rates, label='Win Rate')
    plt.axhline(y=2/3, color='r', linestyle='--', label='Optimal Win Rate (2/3)')
    plt.xlabel('Episodes')
    plt.ylabel('Win Rate')
    plt.title('Win Rate of Q-Learning Agent Over Episodes')
    plt.legend()
    plt.show()

    # Plot Q-values over episodes for the contestant agent
    plt.figure(figsize=(10, 6))
    plt.plot(agent.Q_table, label='Agent Q-values')
    plt.xlabel('Episodes')
    plt.ylabel('Q-values')
    plt.title('Q-values of Q-Learning Agent Over Episodes')
    plt.legend()
    plt.show()

    # Plot Q-values over episodes for Monty
    plt.figure(figsize=(10, 6))
    plt.plot(monty_agent.Q_table, label='Monty Q-values')
    plt.xlabel('Episodes')
    plt.ylabel('Q-values')
    plt.title('Q-values of Monty Agent Over Episodes')
    plt.legend()
    plt.show()
