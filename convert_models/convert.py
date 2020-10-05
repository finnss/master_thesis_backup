import tensorflow as tf
from stable_baselines import TD3
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2
import time
import os

max_depth = 5
max_width_exponent = 10  # 2^10 = 1024
max_input_exponent = 7  # 2^7 = 128
act_function = tf.nn.relu

width = 1
input_size = 1

for depth in range(1, max_depth + 1):  # num
    while width <= 2 ** max_width_exponent:
        while input_size <= 2 ** max_input_exponent:
            """
    if True:
        if True:
            if True:
                depth = 1
            """
            print('Converting model with depth %d, width %d, and input size %d'
                  % (depth, width, input_size))
            saved_model_dir = "../neural_network_training/dummy_networks/ppo2_dummy_%d_%d_%d.zip" \
                % (depth, width, input_size)
            # saved_model_dir = "../trained_models/ppo2_apr6.zip"
            model = PPO2.load(saved_model_dir)

            # TD3
            # converter = tf.lite.TFLiteConverter.from_session(
            # model.sess, [model.observations_ph], [model.policy_out])

            # PPO2
            converter = tf.lite.TFLiteConverter.from_session(
                model.sess, [model.act_model.obs_ph], [model.act_model.policy])
            # converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_SIZE]
            # converter.optimizations = [tf.lite.Optimize.DEFAULT]

            tflite_model = converter.convert()
            base_file_name = 'ppo2_dummy_%d_%d_%d' % (depth, width, input_size)

            with open("dummy_networks/%s.tflite" % base_file_name, "wb") as file:
                # read a list of lines into data
                file.write(tflite_model)

            os.system(
                'xxd -i dummy_networks/%s.tflite > dummy_networks/%s.cpp' % (
                    base_file_name, base_file_name))
            prepend = """# include "%s.h"

// We need to keep the data array aligned on some architectures.
# ifdef __has_attribute
# define HAVE_ATTRIBUTE(x) __has_attribute(x)
# else
# define HAVE_ATTRIBUTE(x) 0
# endif
# if HAVE_ATTRIBUTE(aligned) || (defined(__GNUC__) && !defined(__clang__))
# define DATA_ALIGN_ATTRIBUTE __attribute__((aligned(4)))
# else
# define DATA_ALIGN_ATTRIBUTE
# endif

const """ % base_file_name

            lines = []
            with open('dummy_networks/%s.cpp' % base_file_name, 'r') as file:
                # read a list of lines into data
                lines = file.readlines()
            len_var_index = len(lines) - 1
            len_var_split = lines[len_var_index].split(' = ')
            lines[len_var_index] = lines[len_var_index].replace(
                'unsigned', 'const').replace('dummy_networks_', '')
            """
            lines[len_var_index] = "const int ppo2_dummy_tflite_len = " + \
                len_var_split[1]
            """
            main_variable_declaration_index = 0
            """
            lines[main_variable_declaration_index] = \
                "const unsigned char ppo2_dummy_tflite[] DATA_ALIGN_ATTRIBUTE = {\n"
            """
            lines[main_variable_declaration_index] = lines[main_variable_declaration_index] \
                .replace('[] = {', '[] DATA_ALIGN_ATTRIBUTE = {').replace('dummy_networks_', '')

            # and write everything back
            with open('dummy_networks/%s.cpp' % base_file_name, 'w') as file:
                file.write(prepend)
            with open('dummy_networks/%s.cpp' % base_file_name, 'a') as file:
                file.writelines(lines)

            # header file
            header_content = """# ifndef PPO2_DUMMY_%d_%d_%d_TFLITE
# define PPO2_DUMMY_%d_%d_%d_TFLITE

extern const unsigned char ppo2_dummy_%d_%d_%d_tflite[];
extern const int ppo2_dummy_%d_%d_%d_tflite_len;

# endif
""" % ((depth, width, input_size) * 4)
            os.system('echo "%s" > dummy_networks/%s.h' %
                      (header_content, base_file_name))

            input_size *= 2

        input_size = 1
        width *= 2

    width = 1
