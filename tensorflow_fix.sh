#!/bin/sh
rm -rf arm_mbed/my_uTensor/venv/lib/python3.7/site-packages/tensorflow_core/examples
rm -rf arm_mbed/my_uTensor/venv/lib/python3.7/site-packages/tensorflow_core/tools

cp -r tensorflow/tensorflow/examples arm_mbed/my_uTensor/venv/lib/python3.7/site-packages/tensorflow_core/examples
cp -r tensorflow/tensorflow/tools arm_mbed/my_uTensor/venv/lib/python3.7/site-packages/tensorflow_core/tools