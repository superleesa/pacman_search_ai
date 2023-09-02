import logging
from math import inf
import random

# import util
# from game import Actions, Agent, Directions
# from logs.search_logger import log_function
from pacman import GameState
# from util import manhattanDistance

import util
from game import Actions, Agent, Directions
from pacman import GameState
from util import manhattanDistance
from logs.search_logger import log_function

# from .. import util
# from ..game import Actions, Agent, Directions
# from ..pacman import GameState
# from ..util import manhattanDistance


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class Q2A_Agent(Agent):

    def __init__(self, evalFn='scoreEvaluationFunction', depth='3'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

        # self.weight_food = 10
        # self.weight_scared_ghosts = 30
        # self.weight_health = 100

    @log_function
    def getAction(self, gameState: GameState):
        """
            Returns the minimax action from the current gameState using self.depth
            and self.evaluationFunction.

            Here are some method calls that might be useful when implementing minimax.

            gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

            gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

            gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        logger = logging.getLogger('root')
        logger.info('MinimaxAgent')
        "*** YOUR CODE HERE ***"

        oup = self.alpha_beta_search(gameState)
        print(oup)
        print("======================================")
        return oup

    def alpha_beta_search(self, game_state):
        alpha = -inf
        beta = inf
        return self.max_(game_state, alpha, beta, 0)

    def max_(self, game_state: GameState, alpha: float, beta: float, current_depth: int):
        # base case
        if current_depth == self.depth * game_state.getNumAgents():
            print(scoreEvaluationFunction(game_state))
            return scoreEvaluationFunction(game_state)

        max_backed_up_value = -inf
        max_backed_up_value_action = None
        actions = game_state.getLegalActions(0)

        print("max turn")
        for action in actions:

            successor_state = game_state.generateSuccessor(0, action)
            backed_up_value = self.min_(successor_state, alpha, beta, current_depth + 1)
            if backed_up_value > max_backed_up_value:
                max_backed_up_value = backed_up_value
                max_backed_up_value_action = action


            # beta pruning
            if max_backed_up_value >= beta:
                print("beta cut occured", max_backed_up_value, beta)
                break

            alpha = max(alpha, max_backed_up_value)

        # return state (not evaluation score) if the root node
        if current_depth == 0:
            return max_backed_up_value_action

        # return max_backed_up_value in intermediate MAX nodes
        return max_backed_up_value

    def min_(self, game_state: GameState, alpha: float, beta: float, current_depth):
        """keep calling min until ghost's turn finishes"""

        # base case
        if current_depth == self.depth * game_state.getNumAgents():
            return scoreEvaluationFunction(game_state)

        num_agents = game_state.getNumAgents()
        current_agent = current_depth % num_agents
        next_agent = (current_depth + 1) % num_agents

        # IMPORTANT: if lose (eaten by ghost), this ghost does not have any actions -> just return the score already
        # todo: chnage this from win+lose to something more versaile like
        if game_state.isLose() or game_state.isWin():
            return scoreEvaluationFunction(game_state)


        actions = game_state.getLegalActions(current_agent)
        print("min turn")

        # if next agent is pacman -> stop calling MIN; call MAX
        if next_agent == 0:
            min_backed_up_value = inf
            for action in actions:
                successor_state = game_state.generateSuccessor(current_agent, action)
                backed_up_value = self.max_(successor_state, alpha, beta, current_depth + 1)
                min_backed_up_value = min(min_backed_up_value,
                                          backed_up_value)

                # alpha-pruning
                if min_backed_up_value <= alpha:
                    print("alpha cut occured")
                    break

                beta = min(beta, min_backed_up_value)


        # else (next agent is ghost) -> continue to call min
        else:
            min_backed_up_value = inf
            for action in actions:
                successor_state = game_state.generateSuccessor(current_agent, action)
                min_backed_up_value = min(min_backed_up_value,
                                          self.min_(successor_state, alpha, beta, current_depth + 1))

                # alpha-pruning
                if min_backed_up_value <= alpha:
                    break

                beta = min(beta, min_backed_up_value)

        return min_backed_up_value
