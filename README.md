## Finns master thesis project

### Mbed os examples

#### Setup

1. `cd arm_mbed`
2. `$ brew install mercurial git`
3. `$ brew install https://raw.githubusercontent.com/osx-cross/homebrew-arm/0a6179693c15d8573360c94cee8a60bdf142f7b4/arm-gcc-bin.rb`
4. `$ export GCC_ARM_PATH="<YOUR_PATH_TO_ROOT_FOLDER>/arm_mbed/gcc-arm/bin"`
5. `$ cd <THE_PROJECT_YOU_WANT_TO_COMPILE>`
6. `$ python3 -m venv venv`
7. `$ source venv/bin/activate`
8. `$ pip install --upgrade pip`
9. `$ pip install -r finn_<PROJECT_NAME>_requirements.txt`
10. `$ mbed compile -v --target NRF52_DK --toolchain GCC_ARM --flash`

### For TensorFLow

1. `cd arm_mbed/my_uTensor`
2. `$ pip install -r uTensor_requirements`
3. `$ pip install --upgrade tensorflow`
4. `$ pip install --upgrade utensor_cgen`
5. `$ ../../tensorflow_fix.sh` (chmod it if necessary by doing `$ chmod a+rx tensorflow_fix.sh`)

