import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState

from problems.q1b_problem import get_state_key
from problems.q1a_problem import State, get_food_position
from logs.search_logger import log_function

class q1c_problem:
    """
    A search problem associated with finding a path that collects all of the
    food (dots) in a Pacman game.
    Some useful data has been included here for you
    """
    def __str__(self):
        return str(self.__class__.__module__)

    def __init__(self, gameState: GameState):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.startingGameState: GameState = gameState
        self.num_food_initial = gameState.getNumFood()

        # need to book keep all discovered states
        self.all_states = {}

    @log_function
    def getStartState(self):
        "*** YOUR CODE HERE ***"
        initial_state = State(self.startingGameState)
        self.all_states[get_state_key(initial_state)] = initial_state
        return initial_state

    @log_function
    def isGoalState(self, state):
        "*** YOUR CODE HERE ***"
        # if there is no food at all, it's a goal
        return get_food_position(state.game_state.getFood().asList()) is None

    @log_function
    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """
        "*** YOUR CODE HERE ***"
        successors = []
        legal_actions = state.game_state.getLegalActions(0)
        for action in legal_actions:
            # ignore stop move
            if action is Directions.STOP:
                continue

            successor = state.game_state.generateSuccessor(0, action)
            successor_state = State(successor)
            # state_key = state.game_state.getPacmanPosition()
            state_key = get_state_key(successor_state)
            if state_key in self.all_states:
                successor_state = self.all_states[state_key]
            else:
                self.all_states[state_key] = successor_state

            step_cost = state.g + 1  # step cost always 1 in this problem
            print(step_cost)
            successors.append((successor_state, action, step_cost))

        return successors

