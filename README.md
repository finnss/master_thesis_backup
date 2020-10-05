## Finns master thesis project

NB! This README is only half up-to-date, and the repo contains a decent number of files that are safely ignored. 
Cleanup such as gitignoring venvs, removing temporary files, etc, has not been done.

### Generate dummy networks 

1. `$ cd neural_network_training`
2. `$ python3 -m venv venv`
3. `$ source venv/bin/activate`
4. `$ pip install -r requirements.txt`
5. Chances are unfortuantely good something will go wrong with tensorflow at this point. Google your way around different python versions, different tensorflow version, and other more hacky fixes until it works. Sorry.
6. `$ python train.py`

This will create a large amount of neural networks with random weights. In the `train.py` script, you can choose a couple of parameters:
- `input_size`: the number of input neurons to each neural network.
- `max_depth`: the largest depth the script will use for generating dummy networks. All sizes up to and including will be trained (ie 1, 2, 3, etc).
- `max_width_exponent`: the largest width the script will use for generating dummy networks. For example, a value of 10 here means the largest width to be experimented with becomes 2^10 = 1024. Layer sizes of all _powers of 2_ up to and including this value will be generated (ie 1, 2, 4, 8, etc).
- `max_input_exponent`: not currently used, but can be used to test various input sizes instead of a constant one.
- `act_function`: Activation Function for the neural network. Google it.


### Convert dummy networks into Arduino-compatible formats

1. `$ cd convert_models`
2. `$ python3 -m venv venv`
3. `$ source venv/bin/activate`
4. `$ pip install -r requirements.txt`
5. Chances are unfortuantely good something will go wrong with tensorflow at this point. Google your way around different python versions, different tensorflow version, and other more hacky fixes until it works. Sorry.
6. `$ python convert.py`

The conversion script needs to be configured with the same setting as the above `train.py`. The result will be a list of `.cpp` and `.h` files, one pair for each network. These are basically just native C arrays of numbers, which means an Arduino can run them. Taken from https://www.tensorflow.org/lite/microcontrollers/build_convert#model_conversion. 


### Invoke from the networks on actual hardware

1. Acquire a microcontroller – Arduino Nano 33 BLE was used for this project. This guides assumes that hardware.
2. Download the Arduino IDE.
3. Open the Arduino folder of this repo as a project in the IDE.
4. Download required packages in the IDE addon manager (google which, sorry).
5. Run the project. 
6. HINT! If you run into an issue where the Arduino becomes unresponsive, *quickly double click the reset button* to put it into bootloader mode. This is indicated by the LED shining in a gradient fade-in fade-out loop.