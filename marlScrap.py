import matplotlib.pyplot as plt
import random

class MontyHallEnvironment:
    def __init__(self):
        self.doors = ['goat', 'goat', 'car']
        random.shuffle(self.doors)

    def reset(self):
        self.__init__()

    def get_state(self):
        return self.doors.copy()

    def open_door(self, door_index):
        if self.doors[door_index] == 'car':
            return 1  # Win
        else:
            return 0  # Lose

    def get_available_doors(self):
        return [i for i, door in enumerate(self.doors) if door == 'goat']

    def print_state(self):
        print("Doors:", self.doors)


class MontyhallAgent:
    def __init__(self):
        self.revealed_door = None

    def reveal_door(self, env):
        available_doors = env.get_available_doors()
        chosen_door = random.choice(available_doors)
        self.revealed_door = chosen_door
        return chosen_door

    def reset(self):
        self.revealed_door = None


class ContestantAgent:
    def __init__(self):
        pass

    def choose_door(self, env):
        return random.randint(0, 2)

    def reset(self):
        pass


class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.99, exploration_rate=0.1):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_values = {}  # Dictionary to store Q-values

    def reset(self):
        # Reset the Q-values dictionary
        self.q_values = {}

    def choose_door(self, env):
        # Implement the epsilon-greedy policy to choose an action (door)
        state = str(env.get_state())
        if random.uniform(0, 1) < self.exploration_rate or state not in self.q_values:
            # Explore: choose a random action (door)
            return random.choice(env.get_available_doors())
        else:
            # Exploit: choose the action (door) with the highest Q-value
            return max(self.q_values[state], key=self.q_values[state].get)

    def update_Q_value(self, state, action, reward, next_state):
        # Update the Q-value based on the Bellman equation
        if state not in self.q_values:
            self.q_values[state] = {}
        if next_state not in self.q_values:
            self.q_values[next_state] = {}

        current_q_value = self.q_values[state].get(action, 0)
        max_next_q_value = max(self.q_values[next_state].values(), default=0)
        updated_q_value = current_q_value + self.learning_rate * (reward + self.discount_factor * max_next_q_value - current_q_value)
        self.q_values[state][action] = updated_q_value


if __name__ == "__main__":
    # Initialize environment and agents
    env = MontyHallEnvironment()
    contestant_agent = QLearningAgent()
    monty_agent = MontyhallAgent()

    # Set parameters
    episodes = 1000

    # Lists to store statistics
    total_rewards = []
    win_rates = []

    # Run episodes
    for episode in range(episodes):
        env.reset()
        contestant_agent.reset()
        monty_agent.reset()

        # Play the game
        total_reward = 0
        wins = 0
        for _ in range(3):
            contestant_choice = contestant_agent.choose_door(env)
            monty_revealed = monty_agent.reveal_door(env)
            available_doors = env.get_available_doors()
            if contestant_choice == monty_revealed:
                available_doors.remove(monty_revealed)
                contestant_choice = random.choice(available_doors)
            result = env.open_door(contestant_choice)

            if result == 1:  # Win
                wins += 1
                total_reward += 1
                reward = 1
            else:
                total_reward -= 1
                reward = -1

            # Update Q-values
            next_state = str(env.get_state())
            contestant_agent.update_Q_value(str(env.get_state()), contestant_choice, reward, next_state)

        # Calculate win rate
        win_rate = wins / 3
        win_rates.append(win_rate)

        # Print statistics
        print(f"Episode {episode + 1}: Total Reward = {total_reward}, Win Rate = {win_rate}")
        total_rewards.append(total_reward)

    # Visualize results
    plt.plot(total_rewards)
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title("Total Reward per Episode")
    plt.show()

    plt.plot(win_rates)
    plt.xlabel("Episode")
    plt.ylabel("Win Rate")
    plt.title("Win Rate per Episode")
    plt.show()
