import logging
from math import inf

import util
from problems.q1b_problem import q1b_problem, State

# from .. import util

# NOTE: main parts i changed from the first question is:
# 1) the heuristic: now it uses the distance to the closest food
# 2) the state definition: now a state is uniquely defined by a pair of pacman position AND food positions

def reconstruct_actions(initial_state: State, current_state: State):
    actions = []

    state = current_state
    while state is not initial_state:
        action = state.action_used_to_come_to_this_state
        actions.append(action)

        state = state.prev

    actions.reverse()
    return actions

def get_closest_food_position(current_state):
    current_location = current_state.game_state.getPacmanPosition()

    min_loc = None
    min_distance = inf
    food_array = current_state.game_state.getFood().asList()
    for r in range(len(food_array)):
        for c in range(len(food_array[0])):
            if food_array[r][c]:

                distance = util.manhattanDistance(current_location, (r, c))

                if distance < min_distance:
                    min_distance = distance
                    min_loc = (r, c)
    return min_loc


def heuristic(current_state):
    food_position = get_closest_food_position(current_state)
    pacman_position = current_state.game_state.getPacmanPosition()
    return util.manhattanDistance(pacman_position, food_position)


def q1b_solver(problem: q1b_problem):
    logger = logging.getLogger('root')
    logger.info('question 1b')

    "*** YOUR CODE HERE ***"

    # implement A*
    reached = util.PriorityQueue()
    initial_state = problem.getStartState()
    initial_state.g = 0

    initial_state_h = heuristic(initial_state)
    reached.push(initial_state, (initial_state_h, initial_state_h))

    actions = []
    while reached.count > 0:
        current_state = reached.pop()

        print(current_state.game_state.getPacmanPosition(), current_state.g)

        if problem.isGoalState(current_state):
            actions = reconstruct_actions(initial_state, current_state)
            break

        for reachable_state, action, tentative_cost in problem.getSuccessors(current_state):

            # if never visited => reachable_state.g will return inf => will be OPENED
            # if VISITED and no need to update => will skip this section
            # if VISITED but requires update => will be added to OPEN again (does not happen in this problem)
            # print(tentative_cost, reachable_state.g)
            if tentative_cost < reachable_state.g:

                # do relaxation
                reachable_state.prev = current_state  # redirect pointer
                reachable_state.g = tentative_cost
                h = heuristic(current_state)
                reachable_state.f = h + tentative_cost
                reachable_state.action_used_to_come_to_this_state = action

                if reachable_state not in reached.heap:
                    reached.push(reachable_state, (reachable_state.f, h))

    return actions

