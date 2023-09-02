import logging
from math import inf
import random

# import util
# from game import Actions, Agent, Directions
# from logs.search_logger import log_function
from pacman import GameState
# from util import manhattanDistance

from .. import util
from ..game import Actions, Agent, Directions
from ..pacman import GameState
from ..util import manhattanDistance


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

        return self.alpha_beta_search(gameState)

    def alpha_beta_search(self, game_state):
        alpha = -inf
        beta = inf
        return self.max_(game_state, alpha, beta, 0)

    def max_(self, game_state: GameState, alpha: float, beta: float, current_depth: int):
        # base case
        if current_depth == self.depth * game_state.getNumAgents() - 1:
            return scoreEvaluationFunction(game_state)

        max_backed_up_value = -inf
        max_backed_up_value_action = None
        actions = game_state.getLegalActions(0)
        for action in actions:
            successor_state = game_state.generateSuccessor(0, action)
            backed_up_value = self.min_(successor_state, alpha, beta, current_depth + 1)
            if backed_up_value > max_backed_up_value:
                max_backed_up_value = backed_up_value
                max_backed_up_value_action = action

            # beta pruning
            if max_backed_up_value >= beta:
                break

        # return state (not evaluation score) if the root node
        if current_depth == 0:
            return max_backed_up_value_action

        # return max_backed_up_value in intermediate MAX nodes
        return max_backed_up_value

    def min_(self, game_state: GameState, alpha: float, beta: float, current_depth):
        """keep calling min until ghost's turn finishes"""

        # base case
        if current_depth == self.depth * game_state.getNumAgents() - 1:
            return scoreEvaluationFunction(game_state)

        num_agents = game_state.getNumAgents()
        current_agent = num_agents % current_depth
        next_agent = num_agents % (current_depth + 1)
        actions = game_state.getLegalActions(current_agent)

        # if next agent is pacman -> stop calling MIN; call MAX
        if next_agent == 0:
            min_backed_up_value = inf
            for action in actions:
                successor_state = game_state.generateSuccessor(current_agent, action)
                min_backed_up_value = min(min_backed_up_value,
                                          self.max_(successor_state, alpha, beta, current_depth + 1))

                # alpha-pruning
                if min_backed_up_value <= alpha:
                    break


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

        return min_backed_up_value

    # def evaluate_state(self, game_state: GameState):
    #     """
    #     note: evaluation score bigger the better
    #     """
    #     # number of food collected
    #     num_food_left = game_state.getNumFood()
    #
    #     sum_scared_ghost_time = sum([agent_state.scaredTimer for agent_state in
    #                                  game_state.getGhostStates()])  # sum of time left for scared ghost
    #
    #     pacman_position = game_state.getPacmanPosition()  # next to the ghost means pacman can be killed in the next phase
    #
    #     # get the distance to the closest pacman -> reduce this distance not the sum of the distance to phosts
    #     ghost_positions = game_state.getGhostPositions()
    #     distance_to_closest_ghost = inf
    #     for ghost_position in ghost_positions:
    #         ghost_distance = manhattanDistance(pacman_position, ghost_position)
    #         if ghost_distance < distance_to_closest_ghost:
    #             distance_to_closest_ghost = ghost_distance
    #
    #     # TODO if only one food is left -> add additional score
    #     # TODO more complex conditions if time allows
    #     evaluation_score = - self.weight_food * num_food_left \
    #                        + self.weight_scared_ghosts * sum_scared_ghost_time \
    #                        + self.weight_health * distance_to_closest_ghost
    #
    #     return evaluation_score
