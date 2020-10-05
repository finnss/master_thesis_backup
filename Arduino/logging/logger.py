import serial
import time
from datetime import datetime
from compile_and_transfer import compile_and_transfer
import os

max_depth = 5
max_width_exponent = 10  # 2^10 = 1024
max_input_exponent = 7  # 2^7 = 128

# depth = 2
# widths = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
width = 256


input_size = 8
base_path = '/var/folders/vj/y0q_y7qd5dn8c5pjltk0gngc0000gn/T/arduino_'
debug_logname = "/Users/finn/Documents/skole/master_thesis/Arduino/logging/log_debug.txt"
with open(debug_logname, "w") as file:
    file.write("")

for depth in range(4, max_depth + 1):  # num
    while width <= 2 ** max_width_exponent:

        network_params = "%s_%s_%s" % (depth, width, input_size)
        # timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        logname = "/Users/finn/Documents/skole/master_thesis/Arduino/logging/logs/log_%s.txt" % str(
            network_params)
        with open(logname, "w") as file:
            file.write("")

        compile_output, transfer_output = compile_and_transfer(
            depth, width, input_size)

        compiled_sizes = compile_output \
            .split("\n")[-2] \
            .split('|||')[-1] \
            .replace(' [', '') \
            .replace(']', '') \
            .split(' ')
        print('compiled_sizes:', compiled_sizes)

        success = False
        timestamp = datetime.now().strftime("%d:%m:%Y %H:%M:%S")
        try:
            int(compiled_sizes[0])
            int(compiled_sizes[1])
            int(compiled_sizes[2])

            transfer_conclusion = transfer_output.split("\n")[-3]
            print('transfer_conclusion: ', transfer_conclusion)
            assert(transfer_conclusion[0:7] == "Done in")

            with open(debug_logname, "a") as file:
                file.write("%s\tSuccessfully compiled and transferred network with depth %s and width %s.\n" % (str(timestamp),
                                                                                                                depth, width))
            print("Successfully compiled and transferred network with depth %s and width %s.\n" % (
                depth, width))
            success = True

        except ValueError:
            print('failed')
            build_nr = 5 + depth + width + input_size
            build_path = '%s_build_%d' % (base_path, build_nr)
            cache_path = '%s_cache_%d' % (base_path, build_nr)
            with open(debug_logname, "a") as file:
                file.write("%s\tThis network configuration did NOT compile successfully: depth %s, width %s.\n" % (
                    str(timestamp), depth, width))
            print("This network configuration did NOT compile successfully: depth %s, width %s.\n" % (
                depth, width))

            os.system('rm -rf %s' % build_path)
            os.system('rm -rf %s' % cache_path)
            # width *= 2
            # continue
        except AssertionError:
            print('failed')
            with open(debug_logname, "a") as file:
                file.write("%s\tThis network configuration did NOT transfer successfully: depth %s, width %s.\n" % (
                    str(timestamp), depth, width))
            print("This network configuration did NOT transfer successfully: depth %s, width %s.\n" % (
                depth, width))

            # width *= 2
            # continue
        if not success:
            print("Failed.")
            width *= 2
            continue

        port = "/dev/cu.usbmodem14101"
        arduino = None
        print('Starting to wait...')
        time.sleep(1)
        while True:
            try:
                print("In first try loop...")
                arduino = serial.Serial(port, baudrate=9600, timeout=20)
                if width > 1:
                    arduino.close()
                    arduino.open()
                arduino.flushOutput()
                break
            except (FileNotFoundError, OSError):
                print("Waiting for Arduino...")
        while True:
            try:
                print("In second try loop...")
                arduino.readline()
                break
            except serial.serialutil.SerialException:
                print("Waiting for Arduino...")

                time.sleep(1)
        print('Done waiting.')

        i = 0
        num_iterations = 30
        lines_per_iteration = 15
        while i < num_iterations * lines_per_iteration:
            line = arduino.readline()
            parsed = line.decode("utf-8")
            # print(parsed)
            with open(logname, "a") as file:
                file.write(parsed)
            i += 1

        arduino.close()
        print("Done.")

        width *= 2

    width = 1

# os.system("rm -rf %s*" % base_path)
