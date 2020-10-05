import tensorflow as tf
from stable_baselines import TD3
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2
import time
import os

act_function = tf.nn.relu
width = 1
input_size = 1

# saved_model_dir = "../trained_models/murad.zip"
saved_model_dir = "../neural_network_training/dummy_networks/ppo2_dummy_1_20757_8.zip"
print('Converting model')
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
base_file_name = 'ppo2_dummy_1_20757_8'
open("%s.tflite" % base_file_name, "wb").write(tflite_model)

os.system(
    'xxd -i %s.tflite > %s.h' % (base_file_name, base_file_name))
# include "%s.h"
prepend = """
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

"""

lines = []
with open('%s.h' % base_file_name, 'r') as file:
    # read a list of lines into data
    lines = file.readlines()
len_var_index = len(lines) - 1
len_var_split = lines[len_var_index].split(' = ')
# lines[len_var_index] = lines[len_var_index].replace('unsigned', 'const')
lines[len_var_index] = "const int ppo2_dummy_tflite_len = " + len_var_split[1]

main_variable_declaration_index = 0
lines[
    main_variable_declaration_index] = "const unsigned char ppo2_dummy_tflite[] DATA_ALIGN_ATTRIBUTE = {\n"
# lines[main_variable_declaration_index] = lines[main_variable_declaration_index] \
# .replace('[] = {', '[] DATA_ALIGN_ATTRIBUTE = {')

# and write everything back
with open('%s.h' % base_file_name, 'w') as file:
    file.write(prepend)
with open('%s.h' % base_file_name, 'a') as file:
    file.writelines(lines)
"""
# header file
header_content = """  # ifndef %s_TFLITE
# define %s_TFLITE
"""
extern const unsigned char %s_tflite[];
extern const int %s_tflite_len;
"""
# endif
""" % ((base_file_name,) * 4)
os.system('echo "%s" > %s.h' % (header_content, base_file_name))
"""
