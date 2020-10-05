import os
import matplotlib.pyplot as plt
import numpy as np
import functools
from matplotlib.colors import LogNorm

output = os.popen('ls -la dummy_networks_tflite').read()
lines = output.split('\n')[3:-1]
print(lines[0])
split = list(
    map(lambda y: list(filter(lambda x: x != '', y.split(' '))), lines))
a = split[-1]
all_sizes = list(map(lambda x: [x[-1]] + [x[4]], split))
tflite_sizes = all_sizes[2::3]
formatted_data = []

for i in range(len(tflite_sizes)):
    tflite_size = tflite_sizes[i]
    file_name_split = tflite_size[0].split('_')
    depth = int(file_name_split[2])
    width = int(file_name_split[3])
    input_size = int(file_name_split[4].split('.')[0])
    file_size = int(tflite_size[1])
    formatted_data += [[depth, width, input_size, file_size]]

sorted_data = sorted(formatted_data, key=lambda x: (x[0], x[1], x[2]))
print('sorted_data', sorted_data[0])

with open('read_file_sizes_results.csv', 'w') as file:
    file.write('depth, width, input_size, file_size\n')
with open('read_file_sizes_results.csv', 'a') as file:
    for data in sorted_data:
        file.write('%d, %d, %d, %d\n' %
                   (data[0], data[1], data[2], data[3]))

# Viz
input_size_removed = [[x[0]] + [x[1]] + [x[3]] for x in sorted_data]
duplicates_removed = [v for i, v in enumerate(
    input_size_removed) if i == input_size_removed.index(v)]

with open('read_file_sizes_results_2.csv', 'w') as file:
    file.write('depth, width, file_size\n')
with open('read_file_sizes_results_2.csv', 'a') as file:
    for data in duplicates_removed:
        file.write('%d, %d, %d\n' % (data[0], data[1], data[2]))

plottable_matrix = [[], [], [], [], []]
for e in duplicates_removed:
    depth_index = e[0] - 1
    kilobytes = e[2] / 1000
    plottable_matrix[depth_index] += [kilobytes]
x_below = np.flip(plottable_matrix, 0)

fig = plt.figure()
ax = fig.add_subplot(111)
toshow = ax.matshow(np.array(x_below), extent=[
                    0, 10, 1, 5], norm=LogNorm(vmin=1, vmax=16000))
colorbar = fig.colorbar(toshow, )
colorbar.set_label('Kilobytes')
plt.gca().xaxis.tick_bottom()
ax.set_xticklabels([2 ** x for x in range(0, 20, 2)])
# ax.set_yticklabels(['']+alpha)
ax.set_ylabel('Depth')
ax.set_xlabel('Width')

plt.tight_layout()
plt.show()
