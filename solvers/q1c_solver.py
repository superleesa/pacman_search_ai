import logging
from math import inf

import util
from problems.q1c_problem import q1c_problem, State
from solvers.q1b_solver import reconstruct_actions


# heuristics
def get_foods_and_distances(current_state):
    current_location = current_state.game_state.getPacmanPosition()
    # print(current_location)
    min_loc = None
    min_distance = inf
    max_distance = -inf

    sum_distance = 0

    food_array = current_state.game_state.getFood()
    for x in range(food_array.width):
        for y in range(food_array.height):
            if food_array[x][y]:
                distance = util.manhattanDistance(current_location, (x, y))

                if distance < min_distance:
                    min_distance = distance
                    min_loc = (x, y)

                if distance > max_distance:
                    max_distance = distance

                sum_distance += distance
    mean_distance = sum_distance / current_state.game_state.getNumFood()
    return min_loc, min_distance, max_distance, mean_distance


def get_closest_food_location(current_state):
    current_location = current_state.game_state.getPacmanPosition()

    min_loc = None
    min_distance = inf

    food_array = current_state.game_state.getFood()
    for x in range(food_array.width):
        for y in range(food_array.height):
            if food_array[x][y]:
                distance = util.manhattanDistance(current_location, (x, y))

                if distance < min_distance:
                    min_distance = distance
                    min_loc = (x, y)


    return min_loc

class LocationForPrim:
    def __init__(self, loc):
        self.loc = loc

        self.reached = False
        self.visited = False

        self.distance_to_prev = None

    def __str__(self):
        return str(self.loc)


def get_sum_of_minimum_distances_between_food(current_pacman_loc, food_list_unprocessed):
    # use prims algorithm to find the spanning tree and sum up the total distance

    food_list = []
    for x in range(food_list_unprocessed.width):
        for y in range(food_list_unprocessed.height):
            if food_list_unprocessed[x][y]:
                food_loc = (x, y)
                food = LocationForPrim(food_loc)
                food_list.append(food)


    sum_min_spanning_tree_distance = 0
    reached = util.PriorityQueue()
    current_pacman = LocationForPrim(current_pacman_loc)
    current_pacman.distance_to_prev = 0
    food_list.append(current_pacman)
    reached.push(current_pacman, 0)

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
    # closest_food_loc = get_closest_food_location(current_state)

    # key = hash(current_state.game_state.getFood())
    # if key in min_sp_dists:
    #     sum_min_spanning_tree_distance = min_sp_dists[key]

    sum_min_spanning_tree_distance = get_sum_of_minimum_distances_between_food(current_state.game_state.getPacmanPosition(),
                                                                                   current_state.game_state.getFood())

    # closest_food_loc, min_distance, max_distance, mean_distance = get_foods_and_distances(current_state)

    # num_unvisited_food = get_number_of_unvisited_foods(current_state)
    # num_collected_food = get_number_of_food_collected(current_state, num_food_initial)


    # heurisitcs = [min_distance, max_distance, mean_distance, num_unvisited_food, num_collected_food, sum_min_spanning_tree_distance]




    # if max_or_weighted == "max":
    #     return max(heurisitcs)
    # weights = [1 / 6] * 6
    # return sum([weight*h for weight, h in zip(weights, heurisitcs)])
    return sum_min_spanning_tree_distance

class PriorityQueueWithPeak(util.PriorityQueue):
    def __init__(self):
        super().__init__()

    def peak_min_priority(self):
        return self.heap[0][0]


def q1c_solver(problem: q1c_problem):
    num_initial_food = problem.startingGameState.getNumFood()
    if num_initial_food < 150:
        h_weight = 1
    else:
        h_weight = 10

    # store min spanning tree distances
    # min_sp_dists = dict()

    reached = PriorityQueueWithPeak()
    initial_state = problem.getStartState()
    initial_state.g = 0

    initial_state.h = initial_state.f = heuristic(initial_state, problem.num_food_initial)

    reached.push(initial_state, (initial_state.h, initial_state.h))
    initial_state.in_heap = True


    L = inf  # change this to make the algorithm to DA*
    l = 0
    while l < L and not reached.isEmpty():
        print("==============")
        print(l)
        f_limit = reached.peak_min_priority()

        while not reached.isEmpty() and reached.peak_min_priority() <= f_limit:
            current_state = reached.pop()
            current_state.in_heap = False
            # print(current_state.game_state.getPacmanPosition(), current_state.g)

            if problem.isGoalState(current_state):
                actions = reconstruct_actions(initial_state, current_state)
                return actions

            for reachable_state, action, tentative_cost in problem.getSuccessors(current_state):
                # if never visited => reachable_state.g will return inf => will be OPENED
                # if VISITED and no need to update => will skip this section
                # if VISITED but requires update => will be added to OPEN again (does not happen in this problem)
                # print(tentative_cost, reachable_state.g)
                if tentative_cost < reachable_state.g:
                    # do relaxation
                    reachable_state.prev = current_state  # redirect pointer
                    reachable_state.g = tentative_cost
                    reachable_state.h = heuristic(current_state, problem.num_food_initial)
                    # reachable_state.h = reachable_state.h + (reachable_state.h-current_state.h) + (current_state.g - reachable_state.g)
                    reachable_state.h = reachable_state.h*h_weight
                    reachable_state.f = reachable_state.h + tentative_cost
                    reachable_state.action_used_to_come_to_this_state = action

                    if not reachable_state.in_heap:

                        reached.push(reachable_state, (reachable_state.f, reachable_state.h))
                        reachable_state.in_heap = True

        l += 1

    # could not find a solution
    return None

