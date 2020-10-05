import os

with open('results_flash.csv', 'w') as file:
    file.write('Taken, Percentage\n')

with open('results_ram.csv', 'w') as file:
    file.write('Taken, Percentage, Free\n')

max_depth = 5
max_width_exponent = 10  # 2^10 = 1024
max_input_exponent = 7  # 2^7 = 128

width = 1
input_size = 1

for depth in range(1, max_depth + 1):  # num
    while width <= 2 ** max_width_exponent:
        while input_size <= 2 ** max_input_exponent:
            print('Compiling model with depth %d, width %d, and input size %d'
                  % (depth, width, input_size))

            filename = "./src/dummy_networks/ppo2_dummy_%d_%d_%d.h" % (
                depth, width, input_size)
            modelname = "ppo2_dummy_tflite"

            build_nr = 5 + depth + width + input_size
            base_path = '/var/folders/vj/y0q_y7qd5dn8c5pjltk0gngc0000gn/T/arduino_'
            build_path = '%s_build_%d' % (base_path, build_nr)
            cache_path = '%s_cache_%d' % (base_path, build_nr)
            os.system('mkdir %s' % build_path)
            os.system('mkdir %s' % cache_path)

            compile_command = "/Applications/Arduino.app/Contents/Java/arduino-builder -compile -logger=machine -hardware /Applications/Arduino.app/Contents/Java/hardware -hardware /Users/finn/Library/Arduino15/packages -tools /Applications/Arduino.app/Contents/Java/tools-builder -tools /Applications/Arduino.app/Contents/Java/hardware/tools/avr -tools /Users/finn/Library/Arduino15/packages -built-in-libraries /Applications/Arduino.app/Contents/Java/libraries -libraries /Users/finn/Documents/skole/master_thesis/Arduino/libraries -fqbn=arduino:mbed:nano33ble -vid-pid=0X2341_0X805A -ide-version=10811 -build-path %s -warnings=none -build-cache %s -prefs=build.warn_data_percentage=75 -prefs=runtime.tools.arm-none-eabi-gcc.path=/Users/finn/Library/Arduino15/packages/arduino/tools/arm-none-eabi-gcc/7-2017q4 -prefs=runtime.tools.arm-none-eabi-gcc-7-2017q4.path=/Users/finn/Library/Arduino15/packages/arduino/tools/arm-none-eabi-gcc/7-2017q4 -prefs=runtime.tools.openocd.path=/Users/finn/Library/Arduino15/packages/arduino/tools/openocd/0.10.0-arduino9 -prefs=runtime.tools.openocd-0.10.0-arduino9.path=/Users/finn/Library/Arduino15/packages/arduino/tools/openocd/0.10.0-arduino9 -prefs=runtime.tools.bossac.path=/Users/finn/Library/Arduino15/packages/arduino/tools/bossac/1.9.1-arduino1 -prefs=runtime.tools.bossac-1.9.1-arduino1.path=/Users/finn/Library/Arduino15/packages/arduino/tools/bossac/1.9.1-arduino1 -prefs=build.extra_flags='-DFILENAME=%s -DMODELNAME=%s' -verbose /Users/finn/Documents/skole/master_thesis/Arduino/neural_network_test/neural_network_test.ino" \
                % (build_path, cache_path, filename, modelname)
            print('compile_command:')
            print(compile_command)
            output = os.popen(compile_command).read()
            print("output")
            print(output)
            print("output end")
            lines = output.split('\n')

            flash_mem_line = lines[len(lines) - 3]
            ram_mem_line = lines[len(lines) - 2]

            flash_mem_numbers = flash_mem_line.split(
                '|||')[-1].replace(' [', '').replace(']', '')
            flash_mem_array = flash_mem_numbers.split(
                ' ')  # [taken, max, percent]

            ram_mem_numbers = ram_mem_line.split(
                '|||')[-1].replace(' [', '').replace(']', '')
            ram_mem_array = ram_mem_numbers.split(
                ' ')  # [taken, max, percent, leftover]

            try:
                int(flash_mem_array[0])
                int(flash_mem_array[1])

                with open('results_flash.csv', 'a') as file:
                    taken = int(flash_mem_array[0])
                    percentage = int(flash_mem_array[2])
                    file.write('%d, %d\n' % (taken, percentage))

                with open('results_ram.csv', 'a') as file:
                    taken = int(ram_mem_array[0])
                    percentage = int(ram_mem_array[2])
                    free = int(ram_mem_array[3])
                    file.write('%d, %d, %d\n' % (taken, percentage, free))
            except ValueError:
                print("Not the output we were expecting.")
                with open('results_flash.csv', 'a') as file:
                    file.write('\n')

                with open('results_ram.csv', 'a') as file:
                    file.write('\n')
                # raise RuntimeError("Not the output we were expecting.")
            print('flash_mem_array: ', flash_mem_array)
            print('ram_mem_array: ', ram_mem_array)
            print()

            os.system('rm -rf %s' % build_path)
            os.system('rm -rf %s' % cache_path)

            input_size *= 2

        input_size = 1
        width *= 2

    width = 1
