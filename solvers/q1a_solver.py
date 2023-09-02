import logging

from typing import Optional

import util
from problems.q1a_problem import q1a_problem, State, get_food_position


# from .. import util
# from ..problems.q1a_problem import q1a_problem, State, get_food_position



def reconstruct_actions(initial_state: State, current_state: State):
    actions = []

    state = current_state
    while state is not initial_state:
        action = state.action_used_to_come_to_this_state
        actions.append(action)

        state = state.prev

    actions.reverse()
    return actions

def heuristic(self_position, food_position):
    return util.manhattanDistance(self_position, food_position)

def q1a_solver(problem: q1a_problem):
    "*** YOUR CODE HERE ***"

    # NOTE: position uniquely defines a state

    # implement A*
    reached = util.PriorityQueue()  # note the priority should a form of (f, h)
    initial_state = problem.getStartState()
    initial_state.g = 0

    food_position = get_food_position(initial_state.game_state.getFood().asList())
    initial_state_h = heuristic(initial_state.game_state.getPacmanPosition(), food_position)
    reached.push(initial_state, (initial_state_h, initial_state_h))

    print(food_position)

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
                h = heuristic(current_state.game_state.getPacmanPosition(), food_position)
                reachable_state.f = h + tentative_cost
                reachable_state.action_used_to_come_to_this_state = action


                if reachable_state not in reached.heap:
                    reached.push(reachable_state, (reachable_state.f, h))

    return actions