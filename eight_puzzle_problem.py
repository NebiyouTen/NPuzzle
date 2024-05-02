import numpy as np

class Problem:
    def __ini__(self, N = 3, init_state = None):

        self.N = N
        golden_state = np.zeros(N**2)
        golden_state[:-1] = np.arange(N**2)[1:]

        self.golden_state = golden_state.reshape(N,N)
        if init_state:
            assert init_shape = (N,N)

            self.state = init_state
        else:
            nums = np.arange(N**2)
            np.shuffle(nums)

            self.state = nums.reshape(N,N)

    def is_golden_state(self, state):
        return np.array_equal(state, self.golden_state)
