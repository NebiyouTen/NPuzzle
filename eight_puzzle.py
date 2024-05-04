import os
import sys
import argparse
import numpy as np
import queue
import time
import heapq

from eight_puzzle_problem import NPuzzle
from heuristics import Manhattan, MisplacedTiles, Uniform, get_heuristic

FAILURE_RESULT = "failure"

class Solution:
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
    def __init__(self, state, depth,  heuristic_func):
        self.state = state
        self.depth = depth
        self.heuristic_func = heuristic_func
    @staticmethod
    def CreateNodes(states, depth,  heuristic_func):
        return [ Node(state, depth+1, heuristic_func) for state in states  ]
    def __len__(self):
        return self.state

    def __lt__(self, other):
        self_f_n = self.depth + self.heuristic_func(self.state.state)
        other_f_n = other.depth + self.heuristic_func(other.state.state)

        return self_f_n < other_f_n

class NodesQueue:
    def __init__(self, nodes, algorithm):
        print("creating nodes ", nodes)
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
            print("create FIFO queue ")
            return NodesQueue(nodes, algorithm)
        raise ValueError(f'Invalid {queue_func}')

def general_search(problem, heuristic , search_algorithm):
    node = Node(problem.init_state, 0, heuristic)
    nodes = NodesQueue.CreateQueue([node], search_algorithm)
    print("Initial state: ", problem.init_state)

    print("="*15, f"Starting search: {search_algorithm} ", "="*15)

    count = 0
    solution = Solution()
    solution.initial_state = node
    while True:
        if len(nodes) == 0:
            return FAILURE_RESULT

        node = nodes.get_front()

        # print("Get front ", node.state.state)

        is_golden_state = problem.is_golden_state(node.state)

        print(str(node.state.state), end='\r\033[2A')

        if is_golden_state:
            solution.set_golden_state(node)
            return solution

        expanded_states = problem.expand(node.state)

        expanded_nodes = Node.CreateNodes(expanded_states, node.depth, heuristic)
        solution.num_nodes_expanded += 1

        nodes.queue(expanded_nodes)
        solution.set_max_queue_size(len(nodes))
        # count += 1
        # if count > 200:
        #     break

def main(args):
    '''

    '''
    print('args: ', args)
    # init_state = np.arange(9).reshape(3,3)
    # init_state = np.array([[1,2,3],[4,5,6],[7,8,0]])
    # init_state = np.array([[1,2,3],[4,5,6],[0,7,8]])
    # init_state = np.array([[1,3,6],[5,0,2],[4,7,8]])
    # init_state = np.array([[1,3,6],[5,0,7],[4,8,2]])
    # init_state = np.array([[1,6,7],[5,0,3],[4,8,2]])
    # init_state = np.array([[7,1,2],[4,8,5],[6,3,0]])
    # init_state = np.array([[0,7,2],[4,6,1],[3,5,8]])
    # init_state = np.array([[4,1,2],[5,3,0],[7,8,6]])
    # init_state = np.array([[1,2,0],[4,5,3],[7,8,6]])
    init_state = np.array([[1,5,2],[4,8,7],[6,3,0]])
    # init_state = None

    problem = NPuzzle(init_state = init_state)
    heuristic = get_heuristic(args.heuristic, problem.golden_state.state)
    result = general_search(problem, heuristic, args.algorithm)


    if result == FAILURE_RESULT:
        print("Can not solve puzzle")


    elpased_time = result.end_time - result.start_time
    print("\n\n\n", "="*15, f"Solved ", "="*15)
    print("Summary: " , result)
    print(f"Agorithm: {args.algorithm}, heuristic: ", heuristic)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--algorithm", default = 'uniform',
            choices = ['uniform', 'a_star'],
            help="search algorithm to use")
    parser.add_argument("--heuristic", default = None,
            choices = [None, 'misplaced_tile', 'manhattan'],
            help="heuristic ignored if algorithm is uniform")
    args = parser.parse_args()

    main(args)
