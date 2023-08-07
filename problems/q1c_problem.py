import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions


class q1c_problem:
    """
    A search problem associated with finding a path that collects all of the
    food (dots) in a Pacman game.
    Some useful data has been included here for you
    """

    def __init__(self, gameState):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.startingGameState = gameState

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

