import os


def compile_and_transfer(depth=1, width=1, input_size=1):
    print('Compiling model with depth %d, width %d, and input size %d'
          % (depth, width, input_size))

    filename = "./src/dummy_networks/ppo2_dummy_%d_%d_%d.h" % (
        depth, width, input_size)
    modelname = "ppo2_dummy_tflite"

    build_nr = 5 + depth + width + input_size
    base_path = '/var/folders/vj/y0q_y7qd5dn8c5pjltk0gngc0000gn/T/arduino'
    build_path = '%s_build_%d' % (base_path, build_nr)
    cache_path = '%s_cache_%d' % (base_path, build_nr)
    mkdir_success = os.system('mkdir %s' % build_path) == 0
    print('mkdir_success', mkdir_success)
    compile_output = """
    ||| [0 0 0 0]
    """
    if mkdir_success:
        os.system('mkdir %s' % cache_path)

        compile_command = "/Applications/Arduino.app/Contents/Java/arduino-builder -compile -logger=machine -hardware /Applications/Arduino.app/Contents/Java/hardware -hardware /Users/finn/Library/Arduino15/packages -tools /Applications/Arduino.app/Contents/Java/tools-builder -tools /Applications/Arduino.app/Contents/Java/hardware/tools/avr -tools /Users/finn/Library/Arduino15/packages -built-in-libraries /Applications/Arduino.app/Contents/Java/libraries -libraries /Users/finn/Documents/skole/master_thesis/Arduino/libraries -fqbn=arduino:mbed:nano33ble -vid-pid=0X2341_0X805A -ide-version=10811 -build-path %s -warnings=none -build-cache %s -prefs=build.warn_data_percentage=75 -prefs=runtime.tools.arm-none-eabi-gcc.path=/Users/finn/Library/Arduino15/packages/arduino/tools/arm-none-eabi-gcc/7-2017q4 -prefs=runtime.tools.arm-none-eabi-gcc-7-2017q4.path=/Users/finn/Library/Arduino15/packages/arduino/tools/arm-none-eabi-gcc/7-2017q4 -prefs=runtime.tools.openocd.path=/Users/finn/Library/Arduino15/packages/arduino/tools/openocd/0.10.0-arduino9 -prefs=runtime.tools.openocd-0.10.0-arduino9.path=/Users/finn/Library/Arduino15/packages/arduino/tools/openocd/0.10.0-arduino9 -prefs=runtime.tools.bossac.path=/Users/finn/Library/Arduino15/packages/arduino/tools/bossac/1.9.1-arduino1 -prefs=runtime.tools.bossac-1.9.1-arduino1.path=/Users/finn/Library/Arduino15/packages/arduino/tools/bossac/1.9.1-arduino1 -prefs=build.extra_flags='-DFILENAME=%s -DMODELNAME=%s' -verbose /Users/finn/Documents/skole/master_thesis/Arduino/power_management/power_management.ino" \
            % (build_path, cache_path, filename, modelname)
        compile_output = os.popen(compile_command).read()
        # os.system(compile_command)

        # print("compile_output")
        # print(compile_output)
        # print("compile output end")
        # TODO throw error if compile output unexpected?
    else:
        print("Using existing build...")
    print('hm')
    transfer_command = "/Users/finn/Library/Arduino15/packages/arduino/tools/bossac/1.9.1-arduino1/bossac -d --port=cu.usbmodem14101 -U -i -e -w %s/power_management.ino.bin -R " \
        % (build_path)
    transfer_output = os.popen(transfer_command).read()
    # transfer_output = ""
    # os.system(transfer_command)
    print("transfer_output")
    print(transfer_output)
    print("transfer output end")

    os.system('rm -rf %s' % build_path)
    os.system('rm -rf %s' % cache_path)
    return compile_output, transfer_output
