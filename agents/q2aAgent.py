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

        self.num_paths_with_max_score = 0  # keep track of the paths with the same score as the current max score
        self.prev_turn_action = None
        self.same_as_prev_action_chosen = False
        self.capsule_path_selected = False

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
            return scoreEvaluationFunction(game_state), []

        # if pacman's dead -> return the score already
        if game_state.isLose() or game_state.isWin():
            print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
            return scoreEvaluationFunction(game_state), []

        max_backed_up_value = -inf
        max_backed_up_value_action = None
        actions = game_state.getLegalActions(0)
        shallowest_collected_food_depths = []

        # delete this later on
        scores = []

        print(f"depth {current_depth}, max turn")
        print("actions", actions)
        for action in actions:

            successor_state = game_state.generateSuccessor(0, action)
            collected_food_depths = []
            if self._check_food_has_eaten_in_this_turn(game_state, successor_state):
                collected_food_depths.append(current_depth)

            backed_up_value, collected_food_depths_ancestors = self.min_(successor_state, alpha, beta,
                                                                         current_depth + 1)
            collected_food_depths.extend(collected_food_depths_ancestors)

            # delete this later on
            if current_depth == 0:
                scores.append(backed_up_value)
                print("backed_up_value: ", backed_up_value)

            # check if this value is bigger than the current biggest value
            is_bigger = backed_up_value > max_backed_up_value

            # do tie breaking if it's the root node
            if current_depth == 0:
                has_collected_food_earlier = backed_up_value == max_backed_up_value and self._compare_collected_food_depths(
                    collected_food_depths, shallowest_collected_food_depths)

                # update self.count_same_state to keep track of the paths with the same score as the current max score
                if is_bigger:
                    self.num_paths_with_max_score = 1
                else:
                    self.num_paths_with_max_score += 1

            # choose max (with tie breaking if root node)
            if is_bigger or current_depth == 0 and (
                    has_collected_food_earlier
                    or backed_up_value == max_backed_up_value and self._capsule_tie_breaking(successor_state)
                    or backed_up_value == max_backed_up_value and self._general_tie_breaking(action, max_backed_up_value_action)):

                # if is_bigger or current_depth == 0 and (
                #         has_collected_food_earlier
                #         or backed_up_value == max_backed_up_value and self._general_tie_breaking(action)):

                # update capsule chosen status
                if current_depth == 0 and self._capsule_tie_breaking(successor_state):
                    self.capsule_path_selected = True
                elif current_depth == 0:
                    self.capsule_path_selected = False

                # update same_as_prev_action_chosen status
                if current_depth == 0 and self.same_as_prev_action_chosen:
                    self.same_as_prev_action_chosen = False
                elif current_depth == 0 and action == self.prev_turn_action:
                    self.same_as_prev_action_chosen = True

                max_backed_up_value = backed_up_value
                shallowest_collected_food_depths = collected_food_depths
                max_backed_up_value_action = action


            # beta pruning
            if max_backed_up_value > beta:
                print("beta cut occured", max_backed_up_value, beta)
                break

            alpha = max(alpha, max_backed_up_value)

        # return state (not evaluation score) if the root node
        if current_depth == 0:
            self.prev_turn_action = max_backed_up_value_action
            self.same_as_prev_action_chosen = False
            print(scores)
            return max_backed_up_value_action

        # return max_backed_up_value in intermediate MAX nodes
        return max_backed_up_value, shallowest_collected_food_depths

    def min_(self, game_state: GameState, alpha: float, beta: float, current_depth):
        """keep calling min until ghost's turn finishes"""

        # base case
        if current_depth == self.depth * game_state.getNumAgents():
            return scoreEvaluationFunction(game_state), []

        num_agents = game_state.getNumAgents()
        current_agent = current_depth % num_agents
        next_agent = (current_depth + 1) % num_agents

        # IMPORTANT: if lose (eaten by ghost), this ghost does not have any actions -> just return the score already
        # todo: chnage this from win+lose to something more versaile like
        if game_state.isLose() or game_state.isWin():
            print("lose: score=", scoreEvaluationFunction(game_state))
            return scoreEvaluationFunction(game_state), []

        actions = game_state.getLegalActions(current_agent)
        print(num_agents, current_agent, next_agent)
        print(f"depth {current_depth}, min{current_agent} turn")

        min_backed_up_value = inf
        collected_food_depths_for_min_backed_value_path = []
        for action in actions:
            successor_state = game_state.generateSuccessor(current_agent, action)

            # if next agent is pacman -> stop calling MIN; call MAX
            if next_agent == 0:
                backed_up_value, collected_food_depths_ancestors = self.max_(successor_state, alpha, beta,
                                                                             current_depth + 1)
            # else (next agent is ghost) -> continue to call min
            else:
                backed_up_value, collected_food_depths_ancestors = self.min_(successor_state, alpha, beta,
                                                                             current_depth + 1)

            # update backup value (if needed)
            if backed_up_value < min_backed_up_value:
                min_backed_up_value = backed_up_value
                collected_food_depths_for_min_backed_value_path = collected_food_depths_ancestors  # change found food depths too

            # alpha-pruning
            # note: does not include equal, (if you include, even though there are paths that lead to worse score, this node can be chosen)
            if min_backed_up_value < alpha:
                print("alpha cut occured")
                break

            beta = min(beta, min_backed_up_value)

        return min_backed_up_value, collected_food_depths_for_min_backed_value_path

    def _check_food_has_eaten_in_this_turn(self, previous_state: GameState, current_state: GameState):
        return previous_state.getNumFood() != current_state.getNumFood()

    def _compare_collected_food_depths(self, new_depths, shallowest_depths):
        # assume that if length is different, thier points will be different, so treated by the first condition, not by this function

        # there can be food lists with varying number of foods collected though
        # but, we know that if there is a new path with more food collected, it will be cateched by the first condition
        # what this function implements: if a new path contains the same number of foods with the existing best one
        # hence, the precond: length of new_depths and shallowest_depths are the same, also the integers inside should be ordered
        # assert len(new_depths) == len(shallowest_depths), "length of the new depths list and the shallowest depths list must be the same"

        # if len(new_depths) != len(shallowest_depths)

        for new_path_food_depth, existing_path_food_depth in zip(new_depths, shallowest_depths):
            if new_path_food_depth < existing_path_food_depth:
                return True

        # 0 length will be caught here as well
        return False

    def _capsule_tie_breaking(self, state):
        print("capsule:", state.getCapsules(), state.getPacmanPosition())
        if state.getPacmanPosition() in state.getCapsules():
            self.capsule_path_selected = True
            return True
        return False

    def _general_tie_breaking(self, action, current_max_action):
        # same action should not go into this function twice
        assert self.num_paths_with_max_score != 1, "this function should only be invoked if there are two or more paths" \
                                                   " with the same score; num_paths_with_max_score mean that this is a" \
                                                   " path with new max score -> should not need this method"

        if self.capsule_path_selected:
            return False

        # don't choose a stop action (it likely has no meaning to stop randomly)
        if action == Directions.STOP:
            return False

        # ensure that the pacman can keep the momentum to search through: if there is an action that has the same direction as the previous one, we use it first
        if action == self.prev_turn_action:
            return True

        # if an action that is the same as the previous one is chosen already, keep it (because you don't want to go back)
        if self.same_as_prev_action_chosen:
            return False

        # don't choose the direction opposite to the last path (because you don't want to go back)
        if Actions.reverseDirection(action) == self.prev_turn_action:
            return False

        # if current max action is opposite to the previous action, change it
        if Actions.reverseDirection(current_max_action) == self.prev_turn_action:
            return True


        # ELSE: just choose one of the actions randomly
        weights = [1 / self.num_paths_with_max_score, 1 - 1 / self.num_paths_with_max_score]
        return random.choices([1, 0], weights)[0] == 1
