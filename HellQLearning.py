# import numpy as np
# import random
# import matplotlib.pyplot as plt

# class GameEnv:
#     def __init__(self):
#         # Place the car
#         self.car_index = random.randint(0, 2)
#         # Set Monty's behavior to "Monty from Hell"
#         self.monty = "Monty from Hell"

#         '''
#             "Monty from Hell": The host offers the option to switch
#             only when the player's initial choice is the winning door.
#         '''

#     def open_door(self, initial_index, switch):
#         # Check if Monty is "Monty from Hell"
#         if self.monty == "Monty from Hell":
#             # If the initial choice is the winning door, Monty offers the option to switch
#             if initial_index == self.car_index:
#                 return 0 if switch else 100
#             else:
#                 # Otherwise, proceed with the game as usual
#                 return 100 if initial_index == self.car_index else 0

# class Agent:
#     # Learning rate
#     alpha = 0.11421052631578947

#     def __init__(self):
#         # Initialize the Q-table with zeros
#         self.Q_table = np.zeros(2)

#     def choose_initial_door(self):
#         # Randomly choose the initial door
#         return random.randint(0, 2)

#     def choose_if_switch(self):
#         # Choose whether to switch based on the Q-table
#         return np.argmax(self.Q_table)

#     def update_Q_table(self, action, reward):
#         # Update the Q-table based on the reward received
#         old_q_value = self.Q_table[action]
#         self.Q_table[action] = (1 - self.alpha) * old_q_value + self.alpha * reward

# if __name__ == "__main__":
#     # Define the number of episodes
#     episodes = 1000000
#     agent_reward = 0
#     random_agent_reward = 0
#     agent = Agent()
#     win_counts = 0
#     win_rates = []

#     # Use the greedy exploration policy
#     threshold = 0.2
#     for e in range(episodes):
#         env = GameEnv()
#         # Make less random decisions with more training
#         if e % 100 == 0:
#             threshold /= 2
#         initial_door = agent.choose_initial_door()
#         action = agent.choose_if_switch() if random.uniform(0, 1) > threshold else random.choice([0, 1])
#         r = env.open_door(initial_door, action)
#         agent.update_Q_table(action, r)
#         agent_reward += r
#         # See what randomly switching yields in comparison
#         rand_r = env.open_door(initial_door, random.choice([0, 1]))
#         random_agent_reward += rand_r
#         if r == 100:
#             win_counts += 1
#         win_rates.append(win_counts / (e + 1))

#     # Print cumulative rewards and final Q-value table
#     print('Cumulative agent reward', agent_reward)
#     print('Cumulative agent reward when switching randomly', random_agent_reward)
#     print('Final Q value table:')
#     print('no switch =', agent.Q_table[0], ' switch =', agent.Q_table[1])

#     # Plot the win rates over episodes
#     plt.figure(figsize=(10, 6))
#     plt.plot(win_rates, label='Win Rate')
#     plt.axhline(y=2/3, color='r', linestyle='--', label='Optimal Win Rate (2/3)')
#     plt.xlabel('Episodes')
#     plt.ylabel('Win Rate')
#     plt.title('Win Rate of Q-Learning Agent Over Episodes')
#     plt.legend()
#     plt.show()
import numpy as np
import random
import matplotlib.pyplot as plt

class GameEnv:
    def __init__(self):
        # Place the car
        self.car_index = random.randint(0, 2)
        # Set Monty's behavior to "Monty from Hell"
        self.monty = "Monty from Hell"

        '''
            "Monty from Hell": The host offers the option to switch
            only when the player's initial choice is the winning door.
        '''

    def open_door(self, initial_index, switch):
        # Check if Monty is "Monty from Hell"
        if self.monty == "Monty from Hell":
            # If the initial choice is the winning door, Monty offers the option to switch
            if initial_index == self.car_index:
                return 0 if switch else 100
            else:
                # Otherwise, proceed with the game as usual
                return 100 if initial_index == self.car_index else 0

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
    total_rewards = []

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
        total_rewards.append(agent_reward)

        if (e+1) % 1000 == 0:  # Print progress every 1000 episodes
            print(f"Episode {e+1}: Total Reward = {agent_reward}, Win Rate = {win_counts / (e + 1)}")

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

    # Plot the total rewards over episodes
    plt.figure(figsize=(10, 6))
    plt.plot(total_rewards)
    plt.xlabel('Episodes')
    plt.ylabel('Total Reward')
    plt.title('Total Reward of Q-Learning Agent Over Episodes')
    plt.show()
