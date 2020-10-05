import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib.ticker as ticker

plt.style.use('seaborn-whitegrid')
plt.figure(1)

x = np.linspace(0, 25000, 100)
plt.plot(x, [1024] * len(x), 'k-', label="Arduino Memory Limit")


def visualize(depth, max_width=1050):
    print('Visualizing.')
    colors = ['c', 'r', 'y', 'm', 'g']
    color = colors[depth - 1]

    plt.plot(x, fn(depth, x),  '%s-' % color, label="Depth = %s" % depth)
    plt.legend()
    if depth > 1:
        cross_points = [482, 342, 280, 242]
        cross_point = cross_points[depth - 2]
        plt.plot(cross_point, fn(depth, cross_point), 'ko')
    else:
        a = 23752
        plt.plot(a, fn(depth, a), 'ko')
    #
    # plt.xticks([100, 1000])


# ax = plt.gca()
# plt.xticks([2 ** x for x in range(11)])
# ax.set_xscale('log')
# ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
# plt.ylim(bottom=0, top=20000)
plt.ylabel("Size (KB)")
plt.xlabel("Width")


def fn(depth, x):
    y = depth - 1
    return (4 * x ** 2 * y + 40 * x + 300 * y + 98488) / 1024


visualize(depth=1)
# visualize(depth=2)
# visualize(depth=3)
# visualize(depth=4)
# visualize(depth=5)

plt.show()
