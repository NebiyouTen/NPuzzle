'''
    N_puzzle_search

    This module uses a generic algorithm to implement N-puzzle search.
        Solution: Object to track and store progress as well as solution.
        Node: Implements a node of the search algorithm.
        NodesQueue: FIFO or priority queue implementation.
        general_search: A general search algorithm function.
'''

import os
import sys
import argparse
import numpy as np
import queue
import time
import heapq

from N_puzzle_problem import NPuzzle
from heuristics import Manhattan, MisplacedTiles, Uniform, get_heuristic

FAILURE_RESULT = "failure"

class Solution:
    '''
        Solutions track progress and provide relevant analytics
    '''
    def __init__(self):
        self.start_time = time.time()
        self.solution_state = None
        self.initial_state = None
        self.depth = 0
        self.num_nodes_expanded = 0
        self.max_queue_size = 0

    def set_golden_state(self, state):
        self.solution_state = state
        self.depth = state.depth
        self.end_time = time.time()

    def set_max_queue_size(self, size):
        if size > self.max_queue_size:
            self.max_queue_size = size

    def __str__(self):
        result = f"\n\tSolution state: \n{self.solution_state.state}\n"
        result += f"\t initial_state: \n{self.initial_state.state}\n"
        result += f"\t depth: {self.depth}\n"
        result += f"\t num_nodes_expanded: {self.num_nodes_expanded}\n"
        result += f"\t elapsed_time: {self.end_time - self.start_time:.1f} secs\n"
        result += f"\t max_queue_size: {self.max_queue_size}\n"
        result += f"\t moves: {self.solution_state.state.move_history}\n"

        return result

class Node:
    '''
        Node stores node state, depth, and heuritic value.
    '''
    def __init__(self, state, depth,  heuristic_func):
        self.state = state
        self.depth = depth
        self.heuristic_func = heuristic_func
        self.heuristic = self.heuristic_func(state.state)
        self.is_expanded = False

    @staticmethod
    def CreateNodes(states, depth,  heuristic_func):
        return [ Node(state, depth+1, heuristic_func) for state in states  ]
    def __len__(self):
        return self.state

    def __lt__(self, other):
        self_f_n = self.depth + self.heuristic
        other_f_n = other.depth + other.heuristic

        return self_f_n < other_f_n

class NodesQueue:
    '''
        FIFO or priority queue depending on the search algorithm
    '''
    def __init__(self, nodes, algorithm):
        if algorithm == "a_star":
            self.nodes_queue = []
            for node in nodes:
                heapq.heappush(self.nodes_queue, node)
        else:
            self.nodes_queue = queue.Queue()

            for node in nodes:
                self.nodes_queue.put(node)

        self.algorithm = algorithm

    def get_front(self):
        if self.algorithm == "a_star":
            return heapq.heappop(self.nodes_queue)

        return self.nodes_queue.get()

    def queue(self, nodes):
        for node in nodes:
            if self.algorithm == "a_star":
                heapq.heappush(self.nodes_queue, node)
            else:
                self.nodes_queue.put(node)

    def __len__(self):
        if self.algorithm == "a_star":
            return len(self.nodes_queue)

        return self.nodes_queue.qsize()

    def CreateQueue(nodes, algorithm):
        if algorithm in ["uniform", "a_star"]:
            return NodesQueue(nodes, algorithm)
        raise ValueError(f'Invalid {queue_func}')

def general_search(problem, heuristic , search_algorithm, debug = False, check_repeated = False):
    """
        Perform a general search algorithm on NPuzzle problem.

        Args:
            problem: An instance of the problem to be solved.
            heuristic: A heuristic function used by the search algorithm.
            search_algorithm: The search algorithm to be used.
            debug (optional): A flag indicating whether to print debug information. Default is False.
            check_repeated (optional): A flag indicating whether to check for repeated states during the search. Default is False.

        Returns:
            A solution state or None if no solution is found.
    """

    # create nodes
    node = Node(problem.init_state, 0, heuristic)
    nodes = NodesQueue.CreateQueue([node], search_algorithm)

    if debug:
        print("Initial state: ", problem.init_state)
        print("="*15, f"Starting search: {search_algorithm} ", "="*15)

    count = 0

    # create and track solution objdct
    solution = Solution()
    solution.initial_state = node
    iter = 0
    nodes_so_far = {}

    # search loop
    while True:
        if len(nodes) == 0:
            return FAILURE_RESULT

        # dequeue front node
        node = nodes.get_front()

        exists = False
        # If check_repeated flag, search for repeated. Doesn't really help much.
        if check_repeated:
            for key, arr in nodes_so_far.items():
                if np.array_equal(arr, node.state.state):
                    exists = True
                    break

        if not exists:
            nodes_so_far[iter] = node.state.state

        if debug:
            print(f"iter: {iter}, dequeued: ", node.state.state, f" g(n)={node.depth} , h(n)={node.heuristic} " ,f"exp: {solution.num_nodes_expanded}", f"{len(nodes)}/{solution.max_queue_size}")

        is_golden_state = problem.is_golden_state(node.state)

        # check for golden state
        if is_golden_state:
            solution.set_golden_state(node)
            return solution

        # expand nodes and add children to queue.
        if not exists:
            if debug:
                print("Expanding node: ", node.state)
            expanded_states = problem.expand(node.state)

            expanded_nodes = Node.CreateNodes(expanded_states, node.depth, heuristic)
            solution.num_nodes_expanded += 1
            node.is_expanded = True

            nodes.queue(expanded_nodes)
            solution.set_max_queue_size(len(nodes))

        iter += 1
