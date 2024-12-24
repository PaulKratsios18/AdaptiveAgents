# import numpy as np
# import random
# import matplotlib.pyplot as plt

# class GameEnv:
#     def __init__(self):
#         # place the car
#         self.car_index = random.randint(0, 2)
#         self.monty = "Original"

#     def open_door(self, initial_index, switch):
#         if switch:
#             return 0 if initial_index == self.car_index else 100
#         else:
#             return 100 if initial_index == self.car_index else 0

# class Agent:
#     # learning rate
#     alpha = 0.11421052631578947

#     def __init__(self):
#         # there is only one state, so the table is one dimensional
#         # 0 = don't switch, 1 = switch
#         if (self.alpha > 1 or self.alpha <= 0):
#             raise ValueError('The learning rate should be between zero and one')
#         self.Q_table = np.zeros(2)
    
#     def choose_initial_door(self):
#         return random.randint(0, 2)
    
#     def choose_if_switch(self):
#         return np.argmax(self.Q_table)

#     def update_Q_table(self, action, reward):
#         old_q_value = self.Q_table[action]
#         # there is only one state, so no need to consider the future states
#         self.Q_table[action] = (1-self.alpha)*old_q_value + self.alpha*reward

# if __name__ == "__main__":
#     # Check if a Monty type argument is provided
#     # if len(sys.argv) < 2:
#     #     print("Please provide the Monty type (e.g., 'Ignorant') as an argument.")
#     #     sys.exit(1)

#     # monty_type = sys.argv[1]  # Get the Monty type from the command-line argument

#     episodes = 1000000
#     agent_reward = 0
#     random_agent_reward = 0
#     agent = Agent()
#     win_counts = 0
#     win_rates = []

#     # use the greedy exploration policy
#     threshold = 0.2
#     for e in range(episodes):
#         env = GameEnv()
#         # make less random decisions with more training
#         if e % 100 == 0:
#             threshold /= 2
#         initial_door = agent.choose_initial_door()
#         action = agent.choose_if_switch() if random.uniform(0, 1) > threshold else random.choice([0, 1])
#         r = env.open_door(initial_door, action)
#         agent.update_Q_table(action, r)
#         agent_reward += r
#         # see what randomly switching yields in comparison
#         rand_r = env.open_door(initial_door, random.choice([0, 1]))
#         random_agent_reward += rand_r
#         if r == 100:
#             win_counts += 1
#         win_rates.append(win_counts / (e + 1))

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
        # place the car
        self.car_index = random.randint(0, 2)
        self.monty = "Original"

    def open_door(self, initial_index, switch):
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
    
    def choose_initial_door(self):
        return random.randint(0, 2)
    
    def choose_if_switch(self):
        # Choose whether to switch based on the Q-table
        action = np.argmax(self.Q_table)
        if action == 0:
            self.no_switch_count += 1
        else:
            self.switch_count += 1
        return action

    def update_Q_table(self, action, reward):
        old_q_value = self.Q_table[action]
        self.Q_table[action] = (1-self.alpha)*old_q_value + self.alpha*reward

if __name__ == "__main__":
    episodes = 1000000
    agent_reward = 0
    random_agent_reward = 0
    agent = Agent()
    win_counts = 0
    win_rates = []
    total_rewards = []

    threshold = 0.9
    for e in range(episodes):
        env = GameEnv()  # Pass the Monty type to the GameEnv constructor
        if e % 100 == 0:
            threshold /= 2
        initial_door = agent.choose_initial_door()
        action = agent.choose_if_switch() if random.uniform(0, 1) > threshold else random.choice([0, 1])
        r = env.open_door(initial_door, action)
        agent.update_Q_table(action, r)
        agent_reward += r
        rand_r = env.open_door(initial_door, random.choice([0, 1]))
        random_agent_reward += rand_r
        if r == 100:
            win_counts += 1
        win_rates.append(win_counts / (e + 1))
        total_rewards.append(agent_reward)

        if (e+1) % 1000 == 0:  # Print progress every 1000 episodes
            print(f"Episode {e+1}: Total Reward = {agent_reward}, Win Rate = {win_counts / (e + 1)}")
            print(f"Switch count: {agent.switch_count}, No switch count: {agent.no_switch_count}")
            print(f"Switch percentage: {agent.switch_count / (agent.switch_count + agent.no_switch_count) * 100:.2f}%")
            print(f"No switch percentage: {agent.no_switch_count / (agent.switch_count + agent.no_switch_count) * 100:.2f}%")

    print('Cumulative agent reward', agent_reward)
    print('Cumulative agent reward when switching randomly', random_agent_reward)
    print('Final Q value table:')
    print('no switch =', agent.Q_table[0], ' switch =', agent.Q_table[1])

    plt.figure(figsize=(10, 6))
    plt.plot(win_rates, label='Win Rate')
    plt.axhline(y=2/3, color='r', linestyle='--', label='Optimal Win Rate (2/3)')
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
