'''
    Load outputs file from experiments and generate visuals
'''
import pickle
import numpy as np
import matplotlib.pyplot as plt

with open('results_all.dat', 'rb') as file:
    obj = pickle.load(file)

print(obj)

def avg_by_depth(depth, value):
    # Get unique idx in depth and extract y values by taking the average
    depth_unique = np.unique(depth)
    value_avg = np.array([np.mean([value[i] for i, val in enumerate(depth) if val == idx]) for idx in depth_unique])

    return depth_unique, value_avg

NUM_S = 10
num_nodes_expanded = []
elapsed_time= []
max_queue_size = []
moves = []
depth = []

for res in obj:
    print(res)
    num_nodes_expanded.append(res.num_nodes_expanded)
    elapsed_time.append(res.end_time - res.start_time)
    max_queue_size.append(res.max_queue_size)
    moves.append(res.num_nodes_expanded)
    depth.append(res.depth)

plt.figure()
plt.plot(*avg_by_depth(depth[:NUM_S], num_nodes_expanded[:NUM_S]), label="Uniform C")
plt.plot(*avg_by_depth(depth[NUM_S:NUM_S*2], num_nodes_expanded[NUM_S:NUM_S*2]), label="Misplaced T")
plt.plot(*avg_by_depth(depth[NUM_S*2:], num_nodes_expanded[NUM_S*2:]), label = "Manhattan")
plt.xlabel("Depth")
plt.ylabel("# Expanded Nodes")
plt.legend()
plt.savefig("figures/figure_num_nodes_expanded")
plt.show()


plt.figure()
plt.plot(*avg_by_depth(depth[:NUM_S], elapsed_time[:NUM_S]), label="Uniform C")
plt.plot(*avg_by_depth(depth[:NUM_S], elapsed_time[NUM_S:NUM_S*2]), label="Misplaced T")
plt.plot(*avg_by_depth(depth[:NUM_S], elapsed_time[NUM_S*2:]), label = "Manhattan")
plt.xlabel("Depth")
plt.ylabel("Elapased time (secs)")
plt.legend()
plt.savefig("figures/figure_elapsed_time")
plt.show()


plt.figure()
plt.plot(*avg_by_depth(depth[:NUM_S], max_queue_size[:NUM_S]), label="Uniform C")
plt.plot(*avg_by_depth(depth[:NUM_S], max_queue_size[NUM_S:NUM_S*2]), label="Misplaced T")
plt.plot(*avg_by_depth(depth[:NUM_S], max_queue_size[NUM_S*2:]), label = "Manhattan")
plt.xlabel("Depth")
plt.ylabel("Max queue size")
plt.savefig("figures/figure_max_queue_size")
plt.legend()
plt.show()
