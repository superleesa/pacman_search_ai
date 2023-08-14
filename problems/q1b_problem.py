import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from pacman import GameState


class q1b_problem:
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
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
        util.raiseNotDefined()


    def isGoalState(self, state):
        logger = logging.getLogger('root')
        logger.info('isGoalState')

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


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

        logger = logging.getLogger('root')
        logger.info('getSuccessors')
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

