import logging
import time
from typing import Tuple
from math import inf

import util
from game import Actions, Agent, Directions
from pacman import GameState

# from .. import util
# from ..game import Actions, Agent, Directions
# from ..pacman import GameState

def get_food_position(food_array):
    for r in range(len(food_array)):
        for c in range(len(food_array[0])):
            if food_array[r][c]:
                return r, c

class State:
    # given x and y, this class must be unique
    def __init__(self, game_state):
        self.game_state = game_state

        self.prev = None
        self.g = inf
        self.f = None
        self.action_used_to_come_to_this_state = None


class q1a_problem:
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

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

    def getStartState(self):
        logger = logging.getLogger('root')
        logger.info('getStartState')
        
        "*** YOUR CODE HERE ***"
        initial_state = State(self.startingGameState)
        self.all_states[initial_state.game_state.getPacmanPosition()] = initial_state
        return initial_state


    def isGoalState(self, state: State) -> bool:
        logger = logging.getLogger('root')
        logger.info('isGoalState')

        "*** YOUR CODE HERE ***"

        # if pacman goes to a location where the food is, it will automatically eat it -> no food will be on the map
        return get_food_position(state.game_state.getFood().asList()) is None

    def getSuccessors(self, state: State) -> list[tuple[State, Directions, float]]:
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        logger = logging.getLogger('root')
        logger.info('getSuccessors')

        # ------------------------------------------
        "*** YOUR CODE HERE ***"


        successors = []
        legal_actions = state.game_state.getLegalActions(0)
        for action in legal_actions:
            # ignore stop move
            if action is Directions.STOP:
                continue

            successor = state.game_state.generateSuccessor(0, action)
            if successor.getPacmanPosition() in self.all_states:
                successor_state = self.all_states[successor.getPacmanPosition()]
            else:
                successor_state = State(successor)
                self.all_states[successor_state.game_state.getPacmanPosition()] = successor_state

            step_cost = state.g + 1  # step cost always 1 in this problem
            successors.append((successor_state, action, step_cost))

        return successors



