import os
import sys
import argparse
import numpy as np
import time

from N_puzzle_search import *
from heuristics import *

def main(args):
    '''
        Main function
        arguments:
            args: Command line flags.
    '''
    if args.debug:
        print('args: ', args)

    # If we get initial_state from command line, use it. If not, start from a fixd state
    if len(args.initial_state) > 0:
        N = int((args.N+1)**0.5)
        l = (list(map(int, args.initial_state.split(','))))
        init_state = np.array(l).reshape(N, N)
    else:
        init_state = np.array([[1,5,2],[4,8,7],[6,3,0]])
        N = 3

    '''
        Validate algorithm and heuritic combination.
    '''
    if args.algorithm == 'uniform' and args.heuristic is not None:
        raise ValueError(f"Unsupported heuritic and search algorithm combination: {args.algorithm} not compatible with {args.heuristic}")

    if args.algorithm == 'a_star' and args.heuristic not in ["misplaced_tile", "manhattan"]:
        raise ValueError(f"Unsupported heuritic and search algorithm combination: {args.algorithm} not compatible with {args.heuristic}")

    '''
        Create problem and heuristic objects and pass it the generic search algorithm
    '''
    problem = NPuzzle(init_state = init_state, N=N)
    heuristic = get_heuristic(args.heuristic, problem.golden_state.state)
    result = general_search(problem, heuristic, args.algorithm, args.debug)

    '''
        Search is completed. Let's look at the results.
    '''
    # if failure:
    if result == FAILURE_RESULT:
        print("Can not solve puzzle")
        return

    # If success: print result
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
    parser.add_argument("--N", default = 8,
            type = int,
            help="N-puzzle. Values: 8, 15, 25-puzzle games")
    parser.add_argument("--initial_state", default = "",
            type = str,
            help="CSV of initial state. E.g. Golden state will be '1,2,3,4,5,6,7,8,0'")
    parser.add_argument("--debug", action = 'store_true',
            help="Flag if enabled adds debug information")
    parser.add_argument("--check_repeated", action = 'store_true',
            help="Flag if enabled checks for repated state. Recommened only for Manhattan distance.")

    args = parser.parse_args()

    main(args)
