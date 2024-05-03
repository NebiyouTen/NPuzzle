import os
import sys
import argparse
import numpy as np
import queue

from eight_puzzle_problem import NPuzzle

FAILURE_RESULT = "failure"

class Node:
    def __init__(self, state, depth = 0):
        self.state = state
        self.depth = depth
    @staticmethod
    def CreateNodes(states, depth = 0):
        return [ Node(state, depth = depth+1) for state in states  ]
    def __len__(self):
        return self.state

class NodesQueue:
    def __init__(self, nodes):
        print("creating nodes ", nodes)
        self.nodes_queue = queue.Queue()

        for node in nodes:
            self.nodes_queue.put(node)

    def get_front(self):
        return self.nodes_queue.get()

    def queue(self, nodes):
        for node in nodes:
            self.nodes_queue.put(node)

    def __len__(self):
        return self.nodes_queue.qsize()

    def CreateQueue(nodes, queue_func):
        if queue_func == "FIFO":
            print("create FIFO queue ")
            return NodesQueue(nodes)
        raise ValueError(f'Invalid {queue_func}')

def general_search(problem, queue_func = "FIFO"):
    node = Node(problem.init_state)
    nodes = NodesQueue.CreateQueue([node], queue_func)

    count = 0
    while True:
        if len(nodes) == 0:
            return FAILURE_RESULT

        node = nodes.get_front()

        # print("Get front ", node.state.state)

        is_golden_state = problem.is_golden_state(node.state)

        if is_golden_state:
            return node

        expanded_states = problem.expand(node.state)
        expanded_nodes = Node.CreateNodes(expanded_states, node.depth)

        nodes.queue(expanded_nodes)
        # count += 1
        # if count > 200:
        #     break

def main(args):
    '''

    '''
    print('args: ', args)
    init_state = np.arange(9).reshape(3,3)
    init_state = np.array([[1,2,3],[4,5,6],[7,8,0]])
    init_state = np.array([[1,2,3],[4,5,6],[0,7,8]])
    init_state = np.array([[1,3,6],[5,0,2],[4,7,8]])
    init_state = np.array([[1,3,6],[5,0,7],[4,8,2]])
    init_state = np.array([[1,6,7],[5,0,3],[4,8,2]])
    init_state = np.array([[7,1,2],[4,8,5],[6,3,0]])
    # init_state = np.array([[0,7,2],[4,6,1],[3,5,8]])
    problem = NPuzzle(init_state = init_state)
    result = general_search(problem)

    if result == FAILURE_RESULT:
        print("Can not solve puzzle")


    print(f"Solved: depth: {result.depth}", result.state)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--algorithm", default = 'uniform',
            choices = ['uniform', 'a_star'],
            help="search algorithm to use")
    parser.add_argument("--heuristic", default = None,
            choices = [None, 'misplaced_tile ', 'manhattan'],
            help="heuristic ignored if algorithm is uniform")
    args = parser.parse_args()

    main(args)
