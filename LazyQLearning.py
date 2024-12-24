import numpy as np
import random
import matplotlib.pyplot as plt

class GameEnv:
    def __init__(self):
        # Place the car
        self.car_index = random.randint(0, 2)
        # Set Monty's behavior to "Lazy Monty"
        self.monty = "Lazy Monty"

    '''
        5/9 --> 6/9 Somethings off
        Always open the door closest that does not have a car
        and was not picked by the agent.
    '''
    # def open_door(self, initial_index, switch):   
    #     # Check if Monty is "Lazy Monty"
    #     if self.monty == "Lazy Monty":
    #         # Monty always reveals the door closest to him that does not have the car
    #         if switch:
    #             # If the player switches, return 100 if the car is behind the initial choice, else return 0
    #             return 100 if initial_index == self.car_index else 0
    #         else:
    #             # If the player does not switch, return 100 if the car is not behind the initial choice, else return 0
    #             return 100 if initial_index != self.car_index else 0

    # def open_door(self, initial_index, switch):
    #     # Check if Monty is "Lazy Monty"
    #     if self.monty == "Lazy Monty":
    #         # Monty always reveals the door closest to him that does not have the car
    #         opened_door = [n for n in [0,1,2] if n != self.car_index and n != initial_index]
    #         if switch:
    #             return 0 if initial_index == self.car_index else 100
    #         else:
    #             return 100 if initial_index == self.car_index else 0

    def open_door(self, initial_index, switch):
        # Check if Monty is "Lazy Monty"
        if self.monty == "Lazy Monty":
            # Monty always reveals the door closest to him that does not have the car
            if self.car_index == 0:
                return 0 if initial_index == 1 else 100
            elif self.car_index == 1:
                return 0 if initial_index == 0 else 100
            else:
                # car_index == 2
                return 100 if initial_index == 0 else 0

class Agent:
    # Learning rate
    alpha = 0.11421052631578947

    def __init__(self):
        # Initialize the Q-table with zeros
        self.Q_table = np.zeros(2)

    def choose_initial_door(self):
        # Randomly choose the initial door
        return random.randint(0, 2)

    def choose_if_switch(self):
        # Choose whether to switch based on the Q-table
        return np.argmax(self.Q_table)

    def update_Q_table(self, action, reward):
        # Update the Q-table based on the reward received
        old_q_value = self.Q_table[action]
        self.Q_table[action] = (1 - self.alpha) * old_q_value + self.alpha * reward

if __name__ == "__main__":
    # Define the number of episodes
    episodes = 1000000
    agent_reward = 0
    random_agent_reward = 0
    agent = Agent()
    win_counts = 0
    win_rates = []

    # Use the greedy exploration policy
    threshold = 0.2
    for e in range(episodes):
        env = GameEnv()
        # Make less random decisions with more training
        if e % 100 == 0:
            threshold /= 2
        initial_door = agent.choose_initial_door()
        action = agent.choose_if_switch() if random.uniform(0, 1) > threshold else random.choice([0, 1])
        r = env.open_door(initial_door, action)
        agent.update_Q_table(action, r)
        agent_reward += r
        # See what randomly switching yields in comparison
        rand_r = env.open_door(initial_door, random.choice([0, 1]))
        random_agent_reward += rand_r
        if r == 100:
            win_counts += 1
        win_rates.append(win_counts / (e + 1))

    # Print cumulative rewards and final Q-value table
    print('Cumulative agent reward', agent_reward)
    print('Cumulative agent reward when switching randomly', random_agent_reward)
    print('Final Q value table:')
    print('no switch =', agent.Q_table[0], ' switch =', agent.Q_table[1])

    # Plot the win rates over episodes
    plt.figure(figsize=(10, 6))
    plt.plot(win_rates, label='Win Rate')
    plt.axhline(y=2/3, color='r', linestyle='--', label='Optimal Win Rate (2/3)')
    plt.xlabel('Episodes')
    plt.ylabel('Win Rate')
    plt.title('Win Rate of Q-Learning Agent Over Episodes')
    plt.legend()
    plt.show()
