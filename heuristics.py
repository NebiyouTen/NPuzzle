'''
    heuristics.py. Implementation of different heuristics.
'''
import numpy as np

class MisplacedTiles:
    '''
        Misplaced tile heuritic
    '''
    def __init__(self, golden_state):
        self.golden_state = golden_state

    def __call__(self, state):
        return np.sum((self.golden_state != state).reshape(-1)[:-1])

    def __str__(self):
        return "Misplaced Tile heuristic"

class Manhattan:
    '''
        Manhattan Distance heuristic
    '''
    def __init__(self, golden_state):
        self.golden_state = golden_state

    def __call__(self, state):
        misplaced = self.golden_state[self.golden_state!=state]
        if len(misplaced) == 0:
            return 0

        if misplaced[-1] == 0: misplaced = misplaced[:-1]

        distance = 0
        for item in misplaced:
            if item == 0 : continue
            loc_1_i, loc_1_j = np.where(self.golden_state == item)
            loc_2_i, loc_2_j = np.where(state == item)

            distance += abs(loc_1_i[0] - loc_2_i[0]) + abs(loc_1_j[0] - loc_2_j[0])

        return distance

    def __str__(self):
        return "Manhattan Distance heuristic"

class Uniform:
    '''
        Uniform Cost
    '''
    def __call__(self, state):
        return 0

    def __str__(self):
        return "Uniform Cost (Zero)"

def get_heuristic(heuristic, golden_state):
    if heuristic == "manhattan":
        return Manhattan(golden_state)

    if heuristic == 'misplaced_tile':
        return MisplacedTiles(golden_state)

    return Uniform()

if __name__ == "__main__":
    golden_state = np.array([[1,2,3],[4,5,6],[7,8,0]])

    state_1 = np.array([[1,2,3],[4,5,6],[7,0,8]])
    state_2 = np.array([[2,1,0],[4,5,6],[7,8,3]])
    state_3 = np.array([[1,5,2],[4,8,7],[6,3,0]])

    misplaced_tiles =MisplacedTiles(golden_state)
    manhattan =Manhattan(golden_state)

    print(misplaced_tiles(golden_state))
    print(misplaced_tiles(state_1))
    print(misplaced_tiles(state_2))

    state_4 = np.array([[3,2,8],[4,5,6],[7,1,0]])
    print(manhattan(golden_state))
    print(manhattan(state_3))
    print(manhattan(state_4))
