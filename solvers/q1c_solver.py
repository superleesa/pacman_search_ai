import logging
from math import inf

import util
from problems.q1c_problem import q1c_problem, State
from solvers.q1b_solver import reconstruct_actions


# heuristics
def get_foods_and_distances(current_state):
    current_location = current_state.game_state.getPacmanPosition()
    print(current_location)
    min_loc = None
    min_distance = inf
    max_distance = -inf

    sum_distance = 0

    food_array = current_state.game_state.getFood()
    for x in range(food_array.width):
        for y in range(food_array.height):
            if food_array[x][food_array.height-y-1]:
                distance = util.manhattanDistance(current_location, (x, y))

                if distance < min_distance:
                    min_distance = distance
                    min_loc = (x, y)

                if distance > max_distance:
                    max_distance = distance

                sum_distance += distance
    mean_distance = sum_distance / current_state.game_state.getNumFood()
    return min_loc, min_distance, max_distance, mean_distance


class FoodObjectForPrim:
    def __init__(self, loc):
        self.loc = loc

        self.reached = False
        self.visited = False

        self.distance_to_prev = None

    def __str__(self):
        return str(self.loc)


def get_sum_of_minimum_distances_between_food(closest_food_loc, food_list_unprocessed):
    # use prims algorithm to find the spanning tree and sum up the total distance

    food_list = []
    closest_food = None
    for x in range(food_list_unprocessed.width):
        for y in range(food_list_unprocessed.height):
            if food_list_unprocessed[x][food_list_unprocessed.height - y - 1]:
                food_loc = (x, y)

                if food_loc == closest_food_loc:
                    closest_food = FoodObjectForPrim(food_loc)
                    closest_food.distance_to_prev = 0
                    food_list.append(closest_food)
                else:
                    food = FoodObjectForPrim(food_loc)
                    food_list.append(food)


    sum_min_spanning_tree_distance = 0
    reached = util.PriorityQueue()
    reached.push(closest_food, 0)

    while not reached.isEmpty():
        current_food = reached.pop()
        current_food.visited = True
        sum_min_spanning_tree_distance += current_food.distance_to_prev

        for reachable_food in food_list:
            if reachable_food.loc == current_food.loc:
                continue

            distance = util.manhattanDistance(current_food.loc, reachable_food.loc)
            if not reachable_food.reached and not reachable_food.visited:
                reached.push(reachable_food, distance)
                reachable_food.reached = True
                reachable_food.distance_to_prev = distance

            elif reachable_food.reached and not reachable_food.visited:
                reached.update(reachable_food, distance)
                reachable_food.distance_to_prev = distance

    return sum_min_spanning_tree_distance

def get_number_of_unvisited_foods(current_state):
    return current_state.game_state.getNumFood()

def get_number_of_food_collected(current_state, num_food_initial):
    return num_food_initial - current_state.game_state.getNumFood()


def heuristic(current_state, num_food_initial, max_or_weighted="max"):


    closest_food_loc, min_distance, max_distance, mean_distance = get_foods_and_distances(current_state)
    num_unvisited_food = get_number_of_unvisited_foods(current_state)
    num_collected_food = get_number_of_food_collected(current_state, num_food_initial)

    sum_min_spanning_tree_distance = get_sum_of_minimum_distances_between_food(closest_food_loc, current_state.game_state.getFood())
    heurisitcs = [min_distance, max_distance, mean_distance, num_unvisited_food, num_collected_food, sum_min_spanning_tree_distance]
    if max_or_weighted == "max":
        return max(heurisitcs)
    weights = [1 / 6] * 6
    return sum([weight*h for weight, h in zip(weights, heurisitcs)])

def q1c_solver(problem: q1c_problem):
    "*** YOUR CODE HERE ***"
    # implement A*
    reached = util.PriorityQueue()
    initial_state = problem.getStartState()
    initial_state.g = 0

    initial_state_h = heuristic(initial_state, problem.num_food_initial)
    reached.push(initial_state, (initial_state_h, initial_state_h))
    initial_state.in_heap = True

    actions = []
    while reached.count > 0:
        current_state = reached.pop()
        current_state.in_heap = False

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
                g_old = reachable_state.g
                reachable_state.g = tentative_cost
                h = heuristic(current_state, problem.num_food_initial)
                reachable_state.f = h + tentative_cost
                reachable_state.action_used_to_come_to_this_state = action

                if not reachable_state.in_heap:
                    w_min = 10
                    g_ratio = reachable_state.g / g_old
                    adaptive_w = max(g_ratio/(g_ratio-1), w_min)
                    reached.push(reachable_state, (adaptive_w*h+reachable_state.g, h))
                    reachable_state.in_heap = True

    return actions

