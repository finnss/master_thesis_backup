import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib.ticker as ticker

base_folder = "/Users/finn/Documents/skole/master_thesis/Arduino/logging"
with open("%s/interpreted/depth_1.json" % base_folder, "r") as file:
    re = file.read()
    depth_1 = json.loads(re)
with open("%s/interpreted/depth_2.json" % base_folder, "r") as file:
    re = file.read()
    depth_2 = json.loads(re)
with open("%s/interpreted/depth_3.json" % base_folder, "r") as file:
    re = file.read()
    depth_3 = json.loads(re)
with open("%s/interpreted/depth_4.json" % base_folder, "r") as file:
    re = file.read()
    depth_4 = json.loads(re)
with open("%s/interpreted/depth_5.json" % base_folder, "r") as file:
    re = file.read()
    depth_5 = json.loads(re)

print('Done loading files.')
plt.style.use('seaborn-whitegrid')
# y = np.sin(x) + dy * np.random.randn(50)

plt.figure(1)


def visualize(depth=1, width=1, considered_constant='depth'):
    # plt.figure(depth + width)
    print('Visualizing width depth=%s, width=%s, and %s considered constant.' %
          (depth, width, considered_constant))
    if considered_constant == 'depth':
        dataset = {1: depth_1, 2: depth_2,
                   3: depth_3, 4: depth_4, 5: depth_5}[depth]
        y = [x['invocation_mean'] for x in dataset]
        x = [2 ** x for x in range(len(y))]
        variation = [x['invocation_deviation'] for x in dataset]
        plt.xlabel("Width")
        # plt.title("Depth = %s" % depth)
        # ax = plt.gca()
        # ax.set_xscale('log')
        # ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    else:
        correct_widths = [next(y for y in x if y['width'] == width)
                          for x in [depth_1, depth_2, depth_3, depth_4, depth_5]]
        y = [x['power_management_mean'] for x in correct_widths]
        x = list(range(1, 6))
        variation = [x['power_management_deviation'] for x in correct_widths]
        plt.xlabel("Depth")
        plt.title("Width = %s" % width)

    plt.errorbar(x, y, yerr=variation, fmt='o', color='black',
                 ecolor='gray', elinewidth=3, capsize=3, markersize=4)
    plt.plot(x, y, label="Depth = %s" % depth)
    plt.ylim(bottom=0, top=30)
    plt.ylabel("Runtime (ms)")
    plt.legend()
    # plt.xticks(x)


ax = plt.gca()
ax.set_xscale('log')
ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
plt.xticks([2 ** x for x in range(11)])

visualize(depth=1)
visualize(depth=2)
visualize(depth=3)
visualize(depth=4)
visualize(depth=5)

# visualize(width=1, considered_constant="width")
# visualize(width=2, considered_constant="width")
# visualize(width=4, considered_constant="width")
# visualize(width=8, considered_constant="width")
# visualize(width=16, considered_constant="width")
# visualize(width=32, considered_constant="width")
# visualize(width=64, considered_constant="width")
# visualize(width=128, considered_constant="width")
# visualize(width=256, considered_constant="width")
# visualize(width=512, considered_constant="width")
# visualize(width=1024, considered_constant="width")
plt.show()
