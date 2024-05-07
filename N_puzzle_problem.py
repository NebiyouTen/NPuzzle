import numpy as np

class State:
    def __init__(self, N = 3, state = None, moved = None, move_history = ''):
        if state is not None:
            assert state.shape == (N,N), f"{state.shape} != {(N,N)}"

            self.state = np.copy(state)

        else:
            nums = np.arange(N**2)
            np.random.shuffle(nums)

            self.state = nums.reshape(N,N)
            self.move_history = ""

        self.state = self.state.astype(np.int32)
        self.N = N
        self.blank_loc = self.get_blank_loc(self.state)
        self.moved = moved
        self.move_history = move_history

        if moved :
            if len(self.move_history) > 0:
                self.move_history += "->"
            self.move_history += moved

    def get_blank_loc(self, state):
        i, j = np.where(state == 0)
        return i[0], j[0]

    def __str__(self):
        return np.array_str(self.state)

class NPuzzle:
    def __init__(self, N = 3, init_state = None):

        self.N = N
        golden_state = np.zeros(N**2)
        golden_state[:-1] = np.arange(N**2)[1:]

        self.init_state = State(state=init_state, N = N)
        self.golden_state = State(state=golden_state.reshape(N,N), N = N)

    def is_golden_state(self, state):
        # print("Equal ", state.state, self.golden_state.state, np.array_equal(state.state, self.golden_state.state))
        return np.array_equal(state.state, self.golden_state.state)

    def expand(self, state):
        '''
            Return all expanded states
        '''
        expanded_states = []

        left_state = self.move_left(state)
        if left_state:
            expanded_states.append(left_state)

        right_state = self.move_right(state)
        if right_state:
            expanded_states.append(right_state)

        up_state = self.move_up(state)
        if up_state:
            expanded_states.append(up_state)

        down_state = self.move_down(state)
        if down_state:
            expanded_states.append(down_state)

        return expanded_states

    def move_left(self, state):
        i,j = state.blank_loc

        if j == 0 or state.moved == "R":
            return None

        new_state = np.copy(state.state)

        new_state[i,j] = new_state[i, j-1]
        new_state[i, j - 1] = 0

        return State(N = state.N, state=new_state, moved = "L", move_history = state.move_history)

    def move_right(self, state):
        i,j = state.blank_loc

        if j == state.N - 1 or state.moved == "L":
            return None

        new_state = np.copy(state.state)

        new_state[i, j] = new_state[i, j+1]
        new_state[i, j+1] = 0

        return State(N = state.N, state=new_state, moved = "R", move_history = state.move_history)

    def move_up(self, state):
        i,j = state.blank_loc

        if i == 0 or state.moved == "D":
            return None

        new_state = np.copy(state.state)

        new_state[i, j] = new_state[i-1, j]
        new_state[i-1,j] = 0

        return State(N = state.N, state=new_state, moved = "U", move_history = state.move_history)

    def move_down(self,state):
        i,j = state.blank_loc

        if i == state.N - 1 or state.moved == "U":
            return None

        new_state = np.copy(state.state)

        new_state[i, j] = new_state[i+1, j]
        new_state[i+1,j] = 0

        return State(N = state.N, state=new_state, moved = "D", move_history = state.move_history)
