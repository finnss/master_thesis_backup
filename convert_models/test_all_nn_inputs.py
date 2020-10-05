import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(
    model_path="dummy_networks_tflite/ppo2_dummy_2_256_2.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test model on random input data.
input_shape = input_details[0]['shape']

iterations = 200
half_it = (iterations / 2)

output_list = np.array([])
total_matrix = np.array([np.zeros(iterations) for i in range(iterations)])

print('\ti')
print('j\t', end="\t")
for j in range(iterations):
    j_header = round(j / half_it - 1, 2)
    print(j_header, end="\t")
    total_matrix[0][j] = j_header
print()

for i in range(iterations):
    print("\t", end="")
    i_header = round(i / half_it - 1, 2)
    print(i_header, end="\t")

    total_matrix[i][0] = i_header
    for j in range(iterations):
        # random_input = np.random.random_sample(input_shape)
        # normalized_random_input = list(map(lambda x: x * 2 - 1, random_input))

        input_1 = i / half_it - 1
        input_2 = j / half_it - 1
        a = [input_1, input_2] * int(input_shape[1] / 2)
        wide_input = [np.array(a)]

        input_data = np.array(wide_input, dtype=np.float32)
        interpreter.set_tensor(input_details[0]['index'], input_data)

        interpreter.invoke()

        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.

        output_data = interpreter.get_tensor(output_details[0]['index'])
        # print(output_data)
        output_list += [output_data[0][0]]
        # print('{}\t\t{}\t\t{}'.format(round(input_1, 2),
        #                              round(input_2, 2), round(output_data[0][0], 3)))

        output = round(output_data[0][0], 3)
        print(output, end="\t")
        total_matrix[i][j] = output
    print()

    # print(output_list)

total_matrix_2 = np.flip(total_matrix, 0)

print(total_matrix_2[0])
fig = plt.figure()
ax = fig.add_subplot(111)
toshow = ax.matshow(total_matrix_2, extent=[-1, 1, -1, 1])
colorbar = fig.colorbar(toshow)
plt.gca().xaxis.tick_bottom()
# ax.set_xticklabels(['']+alpha)
# ax.set_yticklabels(['']+alpha)
ax.set_ylabel('Input 1')
ax.set_xlabel('Input 2')

print("Input shape: ", input_shape)

plt.show()
