import os
import sys
import argparse
import numpy as np
import queue

class Node:
    def __init__(self, state):
        self.state = state
    def CreateNodes(states):
        return [ Node(state) for state in states  ]
    def __len__(self):
        return self.state

class NodesQueue:
    def __init__(self. nodes):
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
        if queue_func: "FIFO":
            return NodesQueue(nodes)
        raise ValueError(f'Invalid {queue_func}')

def general_search(problem, queue_func = "FIFO"):
    node = Node(problem.init_state)
    nodes = NodesQueue.CreateQueue([node], queue_func)

    while True:
        if len(nodes) == 0:
            return "failure"

        node = nodes.get_front()

        is_golden_state = problem.is_golden_state(node.state)

        if is_golden_state:
            return node

        expanded_states = problem.expand(node.state)
        expanded_nodes = CreateNodes(expanded_states)

        nodes = nodes.queue(expanded_nodes)

def main(args):
    '''

    '''
    print('args: ', args)


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
