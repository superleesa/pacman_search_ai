import logging

from typing import Optional

# import util
# from problems.q1a_problem import q1a_problem


from .. import util
from ..problems.q1a_problem import q1a_problem, State

def get_food_position(food_array) -> Optional[tuple[int, int]]:
    for r in range(len(food_array)):
        for c in range(len(food_array[0])):
            if food_array[r][c] is True:
                return r, c

def reconstruct_actions(initial_state: State, current_state: State):
    actions = []

    state = current_state
    while state != initial_state:
        action = state.action_used_to_come_to_this_state
        actions.append(action)

        state = current_state.prev

    return actions

def heuristic(self_position, food_position):
    return util.manhattanDistance(self_position, food_position)

def q1a_solver(problem: q1a_problem):
    logger = logging.getLogger('root')
    logger.info('question 1a')

    "*** YOUR CODE HERE ***"
    print("comes here=============================")

    # implement A*
    reached = util.PriorityQueue()
    initial_state = problem.getStartState()
    reached.push(initial_state, 0)
    food_position = get_food_position(initial_state.game_start.getFood())

    
    actions = []
    while reached.count > 0:

        # TODO tie breaking
        current_state = reached.pop()

        if problem.isGoalState(current_state):
            actions = reconstruct_actions(initial_state, current_state)
            break

        # print(current_action, current_cost, current_state.getPacmanPosition())

        for reachable_state, action, tentative_cost in problem.getSuccessors(current_state):

            # if never visited => reachable_state.g will return inf => will be OPENED
            # if VISITED and no need to update => will skip this section
            # if VISITED but requires update => will be added to OPEN again
            if tentative_cost < reachable_state.g:

                # do relaxation
                reachable_state.previous = current_state  # redirect pointer
                reachable_state.g = tentative_cost
                h = heuristic(current_state.game_state.getPacmanPosition(), food_position)
                reachable_state.f = h + tentative_cost
                reachable_state.action_used_to_come_to_this_state = action

                if reachable_state not in reached:
                    reached.push(reachable_state, reachable_state.f)


        # for reachable_state, action, step_cost in problem.getSuccessors(current_state):
        #     cost = current_cost + step_cost
        #
        #     if reachable_state not in visited and reachable_state not in reached.heap:
        #         reached.update((reachable_state, action, cost), cost)
        #     elif reachable_state not in visited:
        #         reached.update((reachable_state, action, cost), cost)

            # else: visited already -> don't need to do anything

    print("actions:::::::::", actions)
    return actions
