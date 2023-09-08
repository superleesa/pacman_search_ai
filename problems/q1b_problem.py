import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from problems.q1a_problem import State, get_food_position
from logs.search_logger import log_function


# in this problem, each state is uniquely defined by position (x, y) AND remaining_food
def get_state_key(game_state):
    game_state = game_state.game_state
    all_food = hash(game_state.getFood())
    pacman_position = game_state.getPacmanPosition()
    return pacman_position, all_food

# class StateQ2(State):
#     def __init__(self, game_state):
#         super().__init__(game_state)
#         self.all_food = frozenset(self.game_state.getFood.asList())
#
#     def create_key(self):
#         return self.game_state.getPacmanPosition(), self.all_food
#
#     def _get_all_food_positions_as_tuples(self, food_list):
#         food_positions = []
#
#         for r in range(len(food_list)):
#             for c in range(len(food_list)):
#                 if food_list[r][c]:
#                     food_positions.append((r, c))
#
#         return food_positions

class q1b_problem:
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
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

        # need to book keep all discovered states
        self.all_states = {}

    @log_function
    def getStartState(self):
        "*** YOUR CODE HERE ***"
        initial_state = State(self.startingGameState)
        self.all_states[get_state_key(initial_state.game_state)] = initial_state
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
            state_key = get_state_key(successor)
            if state_key in self.all_states:
                successor_state = self.all_states[state_key]
            else:
                successor_state = State(successor)
                self.all_states[state_key] = successor_state

            step_cost = state.g + 1  # step cost always 1 in this problem
            successors.append((successor_state, action, step_cost))

        return successors

