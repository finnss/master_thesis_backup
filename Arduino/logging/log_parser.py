import serial
import time
from datetime import datetime
import os

base_folder = "/Users/finn/Documents/skole/master_thesis/Arduino/logging/"
all_files = os.popen("ls -la %s/logs" % base_folder).read().split("\n")
all_logs = [x.split(" ")[-1] for x in all_files[3:-1]]

files_to_parse = all_logs
# files_to_parse = ['log_murad.txt']  # achieves single-log functionality

# start_point = "2020_05_06_20_00_23"
start_point = ""
if start_point != "":
    try:
        start_index = all_logs.index('log_%s' % start_point)
        # start_index = next(log for log in all_logs if log[4::] == start_point)
        files_to_parse = all_logs[start_index::]
    except StopIteration:
        raise RuntimeError(
            "File with given start_index was not found: %s" % start_index)

print("Files to parse: %s." % len(files_to_parse))
for i, file_name in enumerate(files_to_parse):
    print("Parsing file %s: %s" % (i + 1, file_name))
    logname = "%s/logs/%s" % (base_folder, file_name)
    entire_file = ""
    with open(logname, "r") as file:
        entire_file = file.read()

    if not len(entire_file) > 10:
        print("Skipping empty log file.")
        continue

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

print("Parsing complete.")
