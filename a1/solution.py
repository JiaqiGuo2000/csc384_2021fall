#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os  # for time functions
from search import *  # for search engines
from sokoban import SokobanState, Direction, PROBLEMS  # for Sokoban specific classes and problems


def sokoban_goal_state(state):
    '''
    @return: Whether all boxes are stored.
    '''
    for box in state.boxes:
        if box not in state.storage:
            return False
    return True


def heur_manhattan_distance(state):
    # IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # We want an admissible heuristic, which is an optimistic heuristic.
    # It must never overestimate the cost to get from the current state to the goal.
    # The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    # When calculating distances, assume there are no obstacles on the grid.
    # You should implement this heuristic function exactly, even if it is tempting to improve it.
    # Your function should return a numeric value; this is the estimate of the distance to the goal.
    manhattan_distance = 0
    for box in state.boxes:
        if box in state.storage:
            continue
        min_distance = 9999
        for storage_point in state.storage:
            if storage_point in state.boxes:
                continue
            curr_distance = abs(storage_point[0] - box[0]) + abs(storage_point[1] - box[1])
            if curr_distance < min_distance:
                min_distance = curr_distance
        manhattan_distance += min_distance
    return manhattan_distance


# SOKOBAN HEURISTICS
def trivial_heuristic(state):
    '''trivial admissible sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
    count = 0
    for box in state.boxes:
        if box not in state.storage:
            count += 1
    return count


def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.
    # 17/20, [9, 10, 19]
    global boxes_previous_state  # using global vars to quickly return previously stored value
    global heur_previous_score
    try:
        if boxes_previous_state == state.boxes:
            heur_previous_score *= 1.01  # penalize the robots for not pushing boxes
            return heur_previous_score
    except NameError:
        pass
    boxes_previous_state = state.boxes

    def dead_game():  # check if the game is dead
        for curr_box in state.boxes:
            if curr_box in state.storage:
                return False
            vectors = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            unmovable = []
            for vector in vectors:
                target_point = (curr_box[0] + vector[0], curr_box[1] + vector[1])
                if not 0 <= target_point[0] < state.width:
                    unmovable.append(1)
                elif not 0 <= target_point[1] < state.height:
                    unmovable.append(1)
                elif target_point in state.obstacles:
                    unmovable.append(1)
                else:
                    unmovable.append(0)
            if unmovable[0] == 1 and unmovable[3] == 1:
                return True
            if unmovable[0] == 1 and unmovable[1] == 1:
                return True
            if unmovable[1] == 1 and unmovable[2] == 1:
                return True
            if unmovable[2] == 1 and unmovable[3] == 1:
                return True

            vectors = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
            unmovable = []
            for vector in vectors:
                target_point = (curr_box[0] + vector[0], curr_box[1] + vector[1])
                if not 0 <= target_point[0] < state.width:
                    unmovable.append(1)
                elif not 0 <= target_point[1] < state.height:
                    unmovable.append(1)
                elif target_point in state.obstacles:
                    unmovable.append(1)
                elif target_point in state.boxes:
                    unmovable.append(1)
                else:
                    unmovable.append(0)
            if unmovable[3] == 1 and unmovable[0] == 1 and unmovable[1] == 1:
                return True
            if unmovable[1] == 1 and unmovable[2] == 1 and unmovable[4] == 1:
                return True
            if unmovable[4] == 1 and unmovable[7] == 1 and unmovable[6] == 1:
                return True
            if unmovable[6] == 1 and unmovable[5] == 1 and unmovable[3] == 1:
                return True
            return False

    if dead_game():  # if so, the estimated cost should be infinite
        heur_previous_score = 9999
        return 9999
    heur_score = 0

    not_completed_boxes = []
    not_completed_slots = []
    storage_points = []
    for box in state.boxes:
        if box not in state.storage:
            not_completed_boxes.append(box)
    for slot in state.storage:
        if slot not in state.boxes:
            not_completed_slots.append(slot)

    for box_index in range(len(not_completed_boxes)):
        min_distance = 999
        curr_index = -1
        for storage_index in range(len(not_completed_slots)):
            if storage_index in storage_points:
                continue
            curr_distance = (abs(not_completed_slots[storage_index][0] - not_completed_boxes[box_index][0]) + abs(not_completed_slots[storage_index][1] - not_completed_boxes[box_index][1]))
            if curr_distance < min_distance:
                min_distance = curr_distance
                curr_index = storage_index
        # [9, 10, 19]
        heur_score += min_distance
        storage_points.append(curr_index)
    #heur_previous_score = heur_score
    return heur_score

def backup_heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.
    # 16/20, [6, 9, 15, 19]
    global boxes_previous_state
    global heur_previous_score
    try:
        if boxes_previous_state == state.boxes:
            if heur_previous_score >= 999:
                heur_previous_score += 10  # do not encourage paths that goes deeper into dead game
            boxes_previous_state = state.boxes
            return heur_previous_score
    except NameError:
        pass
    boxes_previous_state = state.boxes

    def dead_game():
        for curr_box in state.boxes:
            if curr_box in state.storage:
                return False
            vectors = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            unmovable = []
            for vector in vectors:
                target_point = (curr_box[0] + vector[0], curr_box[1] + vector[1])
                if not 0 <= target_point[0] < state.width:
                    unmovable.append(1)
                elif not 0 <= target_point[1] < state.height:
                    unmovable.append(1)
                elif target_point in state.obstacles:
                    unmovable.append(1)
                else:
                    unmovable.append(0)
            if unmovable[0] == 1 and unmovable[3] == 1:
                return True
            if unmovable[0] == 1 and unmovable[1] == 1:
                return True
            if unmovable[1] == 1 and unmovable[2] == 1:
                return True
            if unmovable[2] == 1 and unmovable[3] == 1:
                return True

            vectors = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
            unmovable = []
            for vector in vectors:
                target_point = (curr_box[0] + vector[0], curr_box[1] + vector[1])
                if not 0 <= target_point[0] < state.width:
                    unmovable.append(1)
                elif not 0 <= target_point[1] < state.height:
                    unmovable.append(1)
                elif target_point in state.obstacles:
                    unmovable.append(1)
                elif target_point in state.boxes:
                    unmovable.append(1)
                else:
                    unmovable.append(0)
            if unmovable[3] == 1 and unmovable[0] == 1 and unmovable[1] == 1:
                return True
            if unmovable[1] == 1 and unmovable[2] == 1 and unmovable[4] == 1:
                return True
            if unmovable[4] == 1 and unmovable[7] == 1 and unmovable[6] == 1:
                return True
            if unmovable[6] == 1 and unmovable[5] == 1 and unmovable[3] == 1:
                return True
            return False

    if dead_game():
        heur_previous_score = 999
        return 999
    heur_score = 0

    not_completed_boxes = []
    not_completed_slots = []
    total_boxes = 0
    for box in state.boxes:
        total_boxes += 1
        if box not in state.storage:
            not_completed_boxes.append(box)
    for slot in state.storage:
        if slot not in state.boxes:
            not_completed_slots.append(slot)
    not_completed_boxes.sort()
    not_completed_slots.sort()
    for i in range(len(not_completed_boxes)):
        heur_score += abs(not_completed_boxes[i][0] - not_completed_slots[i][0]) + abs(not_completed_boxes[i][1] - not_completed_slots[i][1])
        #[6, 9, 15, 19]
        #heur_score += (abs(not_completed_boxes[i][0] - not_completed_slots[i][0]) + abs(not_completed_boxes[i][1] - not_completed_slots[i][1])) ** 0.5
        #[9, 10, 11, 15, 17, 19]
    #print(state.boxes)
    #print(state.robots)
    #print(heur_score)

    return heur_score

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0


def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.
    Use this function stub to encode the standard form of weighted A* (i.e. g + w*h)

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    # Many searches will explore nodes (or states) that are ordered by their f-value.
    # For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    # You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    # The function must return a numeric f-value.
    # The value will determine your state's position on the Frontier list during a 'custom' search.
    # You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    f_val = sN.gval + weight * sN.hval
    return f_val


def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of anytime weighted astar algorithm'''

    start_time = os.times()[0]
    curr_weight = weight
    se = SearchEngine('custom', 'full')
    se.init_search(initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn, fval_function=(lambda sN: fval_function(sN, curr_weight)))
    final, stats = se.search(timebound)
    if not final:
        return False
    curr_best_g = final.gval
    curr_best_outcome = final
    print("first: ", curr_best_g)
    while os.times()[0] - start_time < timebound:
        if curr_weight > 3:
            curr_weight = curr_weight ** 0.5
        curr_weight = curr_weight * 0.1
        se = SearchEngine('custom', 'full')
        se.init_search(initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn, fval_function=(lambda sN: fval_function(sN, curr_weight)))
        final, stats = se.search(os.times()[0] - start_time, (9999, 9999, curr_best_g))
        if not final:
            break
        if final.gval < curr_best_g:
            curr_best_g = final.gval
            curr_best_outcome = final
    print("final: ", curr_best_g, curr_weight)
    return curr_best_outcome


def anytime_gbfs(initial_state, heur_fn, timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of anytime greedy best-first search'''

    start_time = os.times()[0]
    se = SearchEngine('best_first', 'full')
    se.init_search(initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn)
    final, stats = se.search(timebound)
    if not final:
        return False
    curr_best_g = final.gval
    curr_best_outcome = final
    print("regular: ", curr_best_g)
    while os.times()[0] - start_time < timebound:
        se = SearchEngine('breadth_first', 'full')
        se.init_search(initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn)
        final, stats = se.search(os.times()[0] - start_time, (curr_best_g, 9999, 9999))
        if not final:
            break
        if final.gval < curr_best_g:
            curr_best_g = final.gval
            curr_best_outcome = final
    print("final: ", curr_best_g)
    return curr_best_outcome
