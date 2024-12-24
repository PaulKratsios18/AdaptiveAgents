import numpy as np
import random
import matplotlib.pyplot as plt
import sys

class GameEnv:
    def __init__(self, montyType):
        # place the car
        self.car_index = random.randint(0, 2)
        self.monty = montyType

    def open_door(self, initial_index, switch):
        if self.monty == "Original":
            if switch:
                return 0 if initial_index == self.car_index else 100
            else:
                return 100 if initial_index == self.car_index else 0
        
        if self.monty == "Angelic":
            # If the agent chooses correct first, they win
            if initial_index == self.car_index:
                return 100
            # If the initial choice is incorrect, Monty offers the option to switch
            elif initial_index != self.car_index:
                return 0 if switch else 100

        if self.monty == "Hell":
            # # If the agent chooses incorrect first, they lose
            # if initial_index != self.car_index:
            #     return 0
            # # If the initial choice is the winning door, Monty offers the option to switch
            # elif initial_index == self.car_index:
            #     print("Opportunity to switch")
            #     return 0 if switch else 100
            # If the initial choice is the winning door, Monty offers the option to switch
            if initial_index == self.car_index:
                return 0 if switch else 100
            else:
                # Otherwise, proceed with the game as usual
                return 100 if initial_index == self.car_index else 0

        if self.monty == "Ignorant":
            # Monty opens a random door that is not the initial door
            while True:
                random_number = random.randint(0, 2)
                if random_number != initial_index:         
                    opened_door = random_number
                    break
            # If Monty opens the door with the car behind it, the contestant loses
            # because they never selected the door with the car behind it
            if opened_door == self.car_index:
                return 0
            else:
                if switch:
                    return 0 if initial_index == self.car_index else 100
                else:
                    return 100 if initial_index == self.car_index else 0

class Agent:
    alpha = 0.11421052631578947

    def __init__(self):
        if (self.alpha > 1 or self.alpha <= 0):
            raise ValueError('The learning rate should be between zero and one')
        self.Q_table = np.zeros(2)
        self.switch_count = 0
        self.no_switch_count = 0
        self.switch_win_count = 0
        self.no_switch_win_count = 0
        self.switch_opportunities = 0
    
    def choose_initial_door(self):
        return random.randint(0, 2)
    
    def choose_if_switch(self):
        # Choose whether to switch based on the Q-table
        action = np.argmax(self.Q_table)
        self.switch_opportunities += 1
        if action == 0:
            self.no_switch_count += 1
        else:
            self.switch_count += 1
        return action

    def update_Q_table(self, action, reward):
        old_q_value = self.Q_table[action]
        self.Q_table[action] = (1-self.alpha)*old_q_value + self.alpha*reward

if __name__ == "__main__":
    episodes = 10
    agent_reward = 0
    random_agent_reward = 0
    agent = Agent()
    win_counts = 0
    switch_win_counts = 0
    no_switch_win_counts = 0
    win_rates = []
    switch_win_rates = []
    no_switch_win_rates = []
    total_rewards = []

    # Check if command-line arguments are provided
    if len(sys.argv) < 2:
        print("Wrong number of arguments. File and Monty Type expected.")
        sys.exit(1)
    montyType = sys.argv[1]

    threshold = 0.2
    for e in range(episodes):
        env = GameEnv(montyType)  # Pass the Monty type to the GameEnv constructor
        if e % 1 == 0:
            threshold /= 2
        initial_door = agent.choose_initial_door()
        action = agent.choose_if_switch() if random.uniform(0, 1) > threshold else random.choice([0, 1])
        r = env.open_door(initial_door, action)
        agent.update_Q_table(action, r)
        agent_reward += r
        total_rewards.append(agent_reward)

        if r == 100:
            win_counts += 1
            if action == 1:  # Switch
                switch_win_counts += 1
            else:  # No switch
                no_switch_win_counts += 1

        win_rates.append(win_counts / (e + 1))
        switch_win_rates.append(switch_win_counts / agent.switch_count if agent.switch_count != 0 else 0)
        no_switch_win_rates.append(no_switch_win_counts / agent.no_switch_count if agent.no_switch_count != 0 else 0)

        if (e+1) % 1 == 0:  # Print progress every 1000 episodes
            print(f"Episode {e+1}: Total Reward = {agent_reward}, Win Rate = {win_counts / (e + 1)}")
            print(f"Switch count: {agent.switch_count}, No switch count: {agent.no_switch_count}")
            if agent.switch_count != 0:
                switch_win_rate = switch_win_counts / agent.switch_count * 100
            else:
                switch_win_rate = "N/A"
            print(f"Switch Win Rate: {switch_win_rate}")
            print(f"No Switch Win Rate: {no_switch_win_counts / agent.no_switch_count * 100:.2f}%")

    print('Cumulative agent reward', agent_reward)

    optimal = 0
    if montyType == "Original":
        optimal = 2/3
    if montyType == "Angelic":
        optimal = 1.0
    if montyType == "Hell":
        optimal = 1/3
    if montyType == "Ignorant":
        optimal = 1/3
    
    plt.figure(figsize=(10, 6))
    plt.plot(win_rates, label='Overall Win Rate')
    plt.plot(switch_win_rates, label='Switch Win Rate')
    plt.plot(no_switch_win_rates, label='No Switch Win Rate')
    plt.axhline(y=optimal, color='r', linestyle='--', label='Optimal Win Rate ('+str(optimal)+')')
    plt.xlabel('Episodes')
    plt.ylabel('Win Rate')
    plt.title('Win Rate of Q-Learning Agent Over Episodes')
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(total_rewards)
    plt.xlabel('Episodes')
    plt.ylabel('Total Reward')
    plt.title('Total Reward of Q-Learning Agent Over Episodes')
    plt.show()
