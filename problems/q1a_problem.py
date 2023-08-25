import logging
import time
from typing import Tuple

# import util
# from game import Actions, Agent, Directions
# from pacman import GameState

from .. import util
from ..game import Actions, Agent, Directions
from ..pacman import GameState


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

    def getStartState(self):
        logger = logging.getLogger('root')
        logger.info('getStartState')
        
        "*** YOUR CODE HERE ***"
        return self.startingGameState


    def isGoalState(self, state):
        logger = logging.getLogger('root')
        logger.info('isGoalState')

        "*** YOUR CODE HERE ***"
        return state.hasFood()

    def getSuccessors(self, state: GameState):
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
        legal_actions = state.getLegalActions(0)

        for action in legal_actions:
            # ignore stop move
            if action is Directions.STOP:
                continue

            successor = state.generateSuccessor(0, action)
            step_cost = 1  # step cost always 1 in this problem
            successors.append((successor, action, step_cost))

        return successors



