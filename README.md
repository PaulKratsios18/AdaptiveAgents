# Project Outline
### Reinforcement Learning
##### The best option I currently know of.
1. **Environment Modeling:**
   - Define the environment, including the possible actions the agent can take (e.g., choosing a door, switching doors).
   - Model the game host's behavior, representing different possible states of knowledge.

2. **State Representation:**
   - Develop a representation of the current state, considering both the player's and the game host's information.

3. **Reward Design:**
   - Define a reward system that provides feedback to the agent based on the outcomes of its actions (winning the car or not).

4. **Q-Learning or Policy Gradient Methods:**
   - Choose a reinforcement learning algorithm such as Q-learning or policy gradient methods.
   - Train the agent to learn an optimal strategy by updating its policy based on the received rewards.

5. **Exploration-Exploitation Balance:**
   - Implement mechanisms for the agent to balance exploration (trying different strategies) and exploitation (using the learned strategy).

6. **Training Iterations:**
   - Run training iterations where the agent interacts with the environment and learns from the game host's actions.
   - Monitor the agent's performance over time.

7. **Strategy Evaluation:**
   - Evaluate the learned strategy and analyze how well the agent adapts to different game host behaviors.

8. **Iterative Refinement:**
   - Refine the agent's learning process based on observations and insights gained during training.

9. **Conclusion and Insights:**
   - Summarize the results and discuss any insights gained from the agent's learning process.

## Other potential algorithms?
### Pattern recognition algorithms
##### Pattern recognition is a form of machine learning, but typically more rule-based and interpretable than some other machine learning methods.

1. **Define Patterns:**
   - Identify potential patterns or regularities in the game host's behavior. This could include patterns related to door selection, frequency of certain actions, or any observable behaviors.

2. **Feature Extraction:**
   - Extract relevant features from the data, such as the sequence of the host's actions or the locations of the car and goats.

3. **Pattern Recognition Algorithm:**
   - Choose a pattern recognition algorithm that fits your problem. This could include simple algorithms like rule-based matching or more sophisticated ones like Hidden Markov Models (HMM) or Sequential Pattern Mining.

4. **Training:**
   - If applicable, train the algorithm on historical data or simulated scenarios where the game host's behavior is known.
   - Adjust the algorithm parameters to fine-tune its ability to recognize patterns.

5. **Real-time Recognition:**
   - In real-time scenarios, allow the algorithm to observe and recognize patterns in the game host's behavior as it unfolds.

6. **Strategy Adjustment:**
   - Based on the recognized patterns, adjust the agent's strategy dynamically. For example, if a certain pattern suggests the host tends to open the door closest to him, the agent might adapt its strategy accordingly.

7. **Monitoring and Refinement:**
   - Continuously monitor the algorithm's performance and refine it as needed based on new observations or insights.

 |--------------------------------------------------------|

### logic-based or rule-based systems
#### Not sure this would really count as 'learning'
1. **Expert Systems:**
   - Develop an expert system where you encode the knowledge and rules about the game and the host's behavior.
   - Use a rule-based inference engine to make decisions based on the encoded knowledge.

2. **Decision Trees:**
   - Build a decision tree to model the decision-making process of the agent.
   - Nodes in the tree represent decision points based on the game state and host's actions, and branches represent possible outcomes.

3. **Finite State Machines (FSM):**
   - Create a finite state machine to model the different states of the game and transitions based on the host's actions.
   - Define rules for decision-making within each state.

4. **Game Theory Strategies:**
   - Explore strategies from game theory, such as Nash equilibrium or mixed strategies, to guide the agent's decisions.

These approaches are more deterministic and rule-driven compared to reinforcement learning. They rely on explicit rules and logic rather than learning through iterative training.
