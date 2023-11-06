# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount=0.9, iterations=100, theta=1e-5):
        self.theta = theta
        self.pq = util.PriorityQueue()  # Priority queue for prioritized updates
        ValueIterationAgent.__init__(self, mdp, discount, iterations)


    def runValueIteration(self):
        # Step 1: Compute predecessors of all states
        predecessors = self.computePredecessors()

        # Step 2: Initialize an empty priority queue
        self.initializePriorityQueue(predecessors)

        # Step 3: Prioritized Sweeping
        for iteration in range(self.iterations):
            if self.pq.isEmpty():
                break

            state = self.pq.pop()
            if not self.mdp.isTerminal(state):
                self.updateValue(state)  # Update the value of the state

            for predecessor in predecessors[state]:
                diff = abs(self.computeValueFromQValues(predecessor) - self.values[predecessor])
                if diff > self.theta:
                    self.pq.update(predecessor, -diff)


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(ValueEstimationAgent):
    def __init__(self, mdp, discount=0.9, iterations=100, theta=1e-5):
        self.theta = theta
        ValueEstimationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        # Step 1: Compute predecessors of all states
        predecessors = {}
        for state in self.mdp.getStates():
            for action in self.mdp.getPossibleActions(state):
                for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                    if prob > 0:
                        if nextState in predecessors:
                            predecessors[nextState].add(state)
                        else:
                            predecessors[nextState] = {state}

        # Step 2: Initialize a priority queue
        priorityQueue = util.PriorityQueue()

        # Step 3 and 4: Update priorities for non-terminal states
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                maxQValue = max([self.computeQValueFromValues(state, action) for action in self.mdp.getPossibleActions(state)])
                diff = abs(self.values[state] - maxQValue)
                priorityQueue.push(state, -diff)  # Negative because we want higher error to have higher priority

        # Step 5: Iterate for 'self.iterations' times
        for iteration in range(self.iterations):
            if priorityQueue.isEmpty():
                break

            state = priorityQueue.pop()
            if not self.mdp.isTerminal(state):
                # Step 6: Update the value of state
                self.values[state] = max([self.computeQValueFromValues(state, action) for action in self.mdp.getPossibleActions(state)])

                # Step 7: Update predecessors
                for predecessor in predecessors[state]:
                    maxQValue = max([self.computeQValueFromValues(predecessor, action) for action in self.mdp.getPossibleActions(predecessor)])
                    diff = abs(self.values[predecessor] - maxQValue)
                    if diff > self.theta:
                        priorityQueue.update(predecessor, -diff)  # Update the priority


    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

