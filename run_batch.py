import os
import sys
import argparse
import numpy as np
import time
import pickle

from N_puzzle_search import *

def main():
    '''

    '''
    states = [
        np.array([[1,2,3],[4,5,6],[7,8,0]]),
        np.array([[1,2,0],[4,5,3],[7,8,6]]),
        np.array([[1,2,3],[4,5,6],[0,7,8]]),
        np.array([[4,1,2],[5,3,0],[7,8,6]]),
        np.array([[1,3,6],[5,0,2],[4,7,8]]),
        np.array([[1,3,6],[5,0,7],[4,8,2]]),
        np.array([[1,6,7],[5,0,3],[4,8,2]]),
        np.array([[1,5,2],[4,8,7],[6,3,0]]),
        np.array([[7,1,2],[4,8,5],[6,3,0]]),
        np.array([[0,7,2],[4,6,1],[3,5,8]]),
    ]
    algs_heuristics = [("uniform", None),("a_star", "misplaced_tile"), ("a_star", "manhattan")]
    # algs_heuristics = [("a_star", "misplaced_tile")]
    # algs_heuristics = [("a_star", "misplaced_tile"), ("a_star", "manhattan")]
    # algs_heuristics = [("a_star", "misplaced_tile"), ("a_star", "manhattan")]
    # algs_heuristics = [("uniform", None)]

    res = []
    N = 3

    for algorithm, heuristic in algs_heuristics:
        print("Running: ",algorithm, heuristic )
        for i, state in enumerate(states):
            print(f"\t Done problem : {i}/{len(states)} ")
            problem = NPuzzle(init_state = state, N=N)
            h_n = get_heuristic(heuristic, problem.golden_state.state)
            result = general_search(problem, h_n, algorithm, debug=False)
            res.append(result)
            # print("resut ", result)

    with open("results_all.dat", "wb") as f:
        pickle.dump(res, f)


if __name__ == "__main__":
    main()
