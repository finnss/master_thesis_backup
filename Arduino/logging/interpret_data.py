import numpy as np
import serial
import time
from datetime import datetime
import os

base_folder = "/Users/finn/Documents/skole/master_thesis/Arduino/logging/"
all_files = os.popen("ls -la %s/parsed_logs" % base_folder).read().split("\n")
all_logs = [x.split(" ")[-1] for x in all_files[3:-1]]

print('all logs:', all_logs)
files_to_interpret = all_logs
# files_to_parse = ['log_murad.txt']  # achieves single-log functionality

# start_point = "2020_05_06_20_00_23"
start_point = ""
if start_point != "":
    try:
        start_index = all_logs.index('log_%s' % start_point)
        # start_index = next(log for log in all_logs if log[4::] == start_point)
        files_to_interpret = all_logs[start_index::]
    except StopIteration:
        raise RuntimeError(
            "File with given start_index was not found: %s" % start_index)

print("Files to interpret: %s." % len(files_to_interpret))
depth_1 = [x for x in files_to_interpret if x[7] == "1"]
depth_2 = [x for x in files_to_interpret if x[7] == "2"]
depth_3 = [x for x in files_to_interpret if x[7] == "3"]
depth_4 = [x for x in files_to_interpret if x[7] == "4"]
depth_5 = [x for x in files_to_interpret if x[7] == "5"]

for i, logs_in_layer in enumerate([depth_1, depth_2, depth_3, depth_4, depth_5]):
    depth = i + 1
    output_filename = "%s/interpreted/depth_%s.json" % (base_folder, depth)

    with open(output_filename, "w") as file:
        file.write("[\n")

    sorted_by_width = sorted(logs_in_layer, key=lambda x: int(x.split("_")[2]))
    print('sorted_by_width', sorted_by_width)
    for j, parsed_log in enumerate(sorted_by_width):
        all_sense_runtimes = []
        all_ble_runtimes = []
        all_invocation_runtimes = []
        all_power_management_runtimes = []
        all_total_runtimes = []
        entire_file = ""
        parsed_log_filename = "%s/parsed_logs/%s" % (base_folder, parsed_log)
        with open(parsed_log_filename, "r") as file:
            entire_file = file.read()

        for data_point in entire_file.split("\n")[:-1]:
            runtimes = data_point.split(",")
            # (sense_time, ble_time, nn_time, power_time, total_time)
            all_sense_runtimes += [int(runtimes[0])
                                   ] if runtimes[0] != ' ' else []
            all_ble_runtimes += [int(runtimes[1])
                                 ] if runtimes[1] != ' ' else []
            all_invocation_runtimes += [int(runtimes[2])
                                        ] if runtimes[2] != ' ' else []
            all_power_management_runtimes += [int(runtimes[3])
                                              ] if runtimes[3] != ' ' else []
            all_total_runtimes += [int(runtimes[4])
                                   ] if runtimes[4] != ' ' else []

        sense_mean = np.mean(all_sense_runtimes)
        sense_deviation = np.std(all_sense_runtimes)
        ble_mean = np.mean(all_ble_runtimes)
        ble_deviation = np.std(all_ble_runtimes)
        invocation_mean = np.mean(all_invocation_runtimes)
        invocation_deviation = np.std(all_invocation_runtimes)
        power_management_mean = np.mean(all_power_management_runtimes)
        power_management_deviation = np.std(all_power_management_runtimes)
        total_mean = np.mean(all_total_runtimes)
        total_deviation = np.std(all_total_runtimes)

        with open(output_filename, "a") as file:
            file.write("\t{\n")
            file_width = parsed_log.split("_")[2]
            file.write('\t\t"width": %s,\n' % file_width)
            file.write('\t\t"sense_mean": %s,\n' % sense_mean)
            file.write('\t\t"sense_deviation": %s,\n' % sense_deviation)
            file.write('\t\t"ble_mean": %s,\n' % ble_mean)
            file.write('\t\t"ble_deviation": %s,\n' % ble_deviation)
            file.write('\t\t"invocation_mean": %s,\n' % invocation_mean)
            file.write('\t\t"invocation_deviation": %s,\n' %
                       invocation_deviation)
            file.write('\t\t"power_management_mean": %s,\n' %
                       power_management_mean)
            file.write('\t\t"power_management_deviation": %s,\n' %
                       power_management_deviation)
            file.write('\t\t"total_mean": %s,\n' % total_mean)
            file.write('\t\t"total_deviation": %s\n' % total_deviation)
            file.write("\t},\n" if j != len(logs_in_layer) - 1 else "\t}\n")

    with open(output_filename, "a") as file:
        file.write("]")


"""
for i, file_name in enumerate(files_to_interpret):
    print("Interpreting file %s: %s" % (i + 1, file_name))
    logname = "%s/logs/%s" % (base_folder, file_name)
    entire_file = ""
    with open(logname, "r") as file:
        entire_file = file.read()

    parsed_filename = logname.replace(
        "/logs/", "/parsed_logs/").replace("log_", "parsed_")

    with open(parsed_filename, "w") as file:
        # file.write("sense, ble, nn, power, total\n")
        file.write("")

    entries = entire_file.split("Loop.")[1::]
    for entry in entries:
        lines = entry.split("\n")

        sense_time = -1
        ble_time = -1
        nn_time = -1
        power_time = -1
        total_time = -1

        for line in [x for x in lines if ":" in x]:
            split_line = line.split(":")
            key = split_line[0]
            value = split_line[1]

            if key == "Cycle time elapsed":
                sense_time = int(value)
            elif key == "BLE time elapsed":
                ble_time = int(value)
            elif key == "After invoke. Time spent":
                nn_time = int(value)
            elif key == "Interpreting NN output...Total invoke time elapsed":
                power_time = int(value)
            elif key == "Total time spent":
                total_time = int(value)

        # if -1 in [sense_time, ble_time, nn_time, power_time, total_time]:
            # print("Warning: Some expected value was not read.")
            # raise RuntimeError("")

        with open(parsed_filename, "a") as file:
            to_write = ("%s, %s, %s, %s, %s\n" %
                        (sense_time, ble_time, nn_time, power_time, total_time))
            empty_entries_fixed = to_write.replace("-1", "")
            file.write(empty_entries_fixed)
"""
print("Interpretation complete.")
