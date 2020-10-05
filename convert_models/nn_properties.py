import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(
    model_path="power_management_model_feb12.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test model on random input data.
input_shape = input_details[0]['shape']

random_input = np.random.random_sample(input_shape)
normalized_random_input = list(map(lambda x: x * 2 - 1, random_input))

input_data = np.array(normalized_random_input, dtype=np.float32)
interpreter.set_tensor(input_details[0]['index'], input_data)

interpreter.invoke()

# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.

output_data = interpreter.get_tensor(output_details[0]['index'])
# print(output_data)
output = output_data[0][0]

print('output', output)
