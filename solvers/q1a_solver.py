import logging

import util
from problems.q1a_problem import q1a_problem


def q1a_solver(problem: q1a_problem):
    logger = logging.getLogger('root')
    logger.info('question 1a')

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()  # Your code replaces this line
    
    # implement A*
    pq = util.PriorityQueue()
    initial_state = problem.getStartState()
    pq.push(initial_state, 0)
    
    actions = []
    while len(pq) > 0:
        
        current_state = pq.pop()
        # TODO covert state to action
        actions.append(current_state)
        
        for reachable_state in problem.getSuccessors(current_state):
            current_state_loc, reachable_state_loc = current_state.getPacmanPosition(), reachable_state.getPacmanPosition()
            cost = util.manhattanDistance(current_state_loc, reachable_state_loc)
            
            # TODO implement "in" method
            if reachable_state in pq:
                pq.update(reachable_state, cost)
            else:
                pq.push(reachable_state, cost)
    
    return actions