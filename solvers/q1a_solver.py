import logging

# import util
# from problems.q1a_problem import q1a_problem

from .. import util
from ..problems.q1a_problem import q1a_problem


def q1a_solver(problem: q1a_problem):
    logger = logging.getLogger('root')
    logger.info('question 1a')

    "*** YOUR CODE HERE ***"
    # implement A*
    pq = util.PriorityQueue()
    initial_state = problem.getStartState()
    pq.push(initial_state, 0)

    visited = set()  # closed
    reached = set()  # opened
    
    actions = []
    while len(reached) > 0:
        
        current_state, current_action = pq.pop()
        actions.append(current_action)
        
        for reachable_state, action, step_cost in problem.getSuccessors(current_state):
            if reachable_state not in visited and reachable_state not in reached:
                pq.update((reachable_state, action), action)
            elif reachable_state not in visited:
                pq.update((reachable_state, action), step_cost)

            # else: visited already -> don't need to do anything
    
    return actions
