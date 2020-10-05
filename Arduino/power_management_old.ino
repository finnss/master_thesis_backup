/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#include <TensorFlowLite.h>

#include "main_functions.h"

#include <Arduino_HTS221.h>
#include "interpret_nn_output.h"
#include "power_management_model_feb12.h"
#include "output_handler.h"
#include <ArduinoBLE.h>
#include "think_cycle.h"
#include "tensorflow/lite/experimental/micro/kernels/micro_ops.h"
#include "tensorflow/lite/experimental/micro/micro_error_reporter.h"
#include "tensorflow/lite/experimental/micro/micro_interpreter.h"
#include "tensorflow/lite/experimental/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/version.h"

// Globals, used for compatibility with Arduino-style sketches.
namespace {
  tflite::ErrorReporter* error_reporter = nullptr;
  const tflite::Model* model = nullptr;
  tflite::MicroInterpreter* interpreter = nullptr;
  TfLiteTensor* model_input = nullptr;
  int input_length;

  // Create an area of memory to use for input, output, and intermediate arrays.
  // The size of this will depend on the model you're using, and may need to be
  // determined by experimentation.
  constexpr int kTensorArenaSize = 60 * 1024;
  uint8_t tensor_arena[kTensorArenaSize];

  // Whether we should clear the buffer next time we fetch data
  bool should_clear_buffer = false;

  int time_to_sleep = 0;
  TfLiteStatus invoke_status;
  bool should_ask_nn = false;
  // Think cycle

  // BLE Battery Level Characteristic
   // BLE Battery Service
  BLEService batteryService("180F");
  BLEUnsignedCharCharacteristic batteryLevelChar("2A19",  // standard 16-bit characteristic UUID
      BLERead | BLENotify); // remote clients will be able to get notifications if this characteristic changes

  int oldBatteryLevel = 0;  // last battery level reading from analog input
  long previousMillis = 0;  // last time the battery level was checked, in ms

}  // namespace

void updateBatteryLevel() {
  /* Read the current voltage level on the A0 analog input pin.
     This is used here to simulate the charge level of a battery.
  */
  int battery = analogRead(A0);
  int batteryLevel = map(battery, 0, 1023, 0, 100);

  if (batteryLevel != oldBatteryLevel) {      // if the battery level has changed
    error_reporter->Report("Battery Level % is now: "); // print it
    error_reporter->Report("%d", batteryLevel);
    batteryLevelChar.writeValue(batteryLevel);  // and update the battery level characteristic
    oldBatteryLevel = batteryLevel;           // save the level for next comparison
  }
}

// The name of this function is important for Arduino compatibility.
void setup() {
  // Set up logging. Google style is to avoid globals or statics because of
  // lifetime uncertainty, but since this has a trivial destructor it's okay.
  static tflite::MicroErrorReporter micro_error_reporter;  // NOLINT
  error_reporter = &micro_error_reporter;

  // Map the model into a usable data structure. This doesn't involve any
  // copying or parsing, it's a very lightweight operation.
  model = tflite::GetModel(power_management_model_feb12);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    error_reporter->Report(
        "Model provided is schema version %d not equal "
        "to supported version %d.",
        model->version(), TFLITE_SCHEMA_VERSION);
    return;
  }


  // Pull in only the operation implementations we need.
  // This relies on a complete list of all the ops needed by this graph.
  // An easier approach is to just use the AllOpsResolver, but this will
  // incur some penalty in code space for op implementations that are not
  // needed by this graph.
  // tflite::micro::AllOpsResolver resolver;

  static tflite::MicroMutableOpResolver micro_mutable_op_resolver;  // NOLINT

  micro_mutable_op_resolver.AddBuiltin(
      tflite::BuiltinOperator_FULLY_CONNECTED,
      tflite::ops::micro::Register_FULLY_CONNECTED());
  micro_mutable_op_resolver.AddBuiltin(
      tflite::BuiltinOperator_RELU,
      tflite::ops::micro::Register_RELU());

  // Build an interpreter to run the model with
  static tflite::MicroInterpreter static_interpreter(
      model, micro_mutable_op_resolver, tensor_arena, kTensorArenaSize,
      error_reporter);
  interpreter = &static_interpreter;

  // Allocate memory from the tensor_arena for the model's tensors
  interpreter->AllocateTensors();

  // Obtain pointer to the model's input tensor
  model_input = interpreter->input(0);
  if ((model_input->dims->size != 4) || (model_input->dims->data[0] != 1) ||
      (model_input->dims->data[1] != 128) ||
      (model_input->dims->data[2] != 3) || // TODO kChannelNumber
      (model_input->type != kTfLiteFloat32)) {
    error_reporter->Report("Bad input tensor parameters in model");
    return;
  }

  input_length = model_input->bytes / sizeof(float);

  // TfLiteStatus setup_status = SetupAccelerometer(error_reporter);
  TfLiteStatus setup_status = kTfLiteOk;
  if (setup_status != kTfLiteOk) {
    error_reporter->Report("Set up failed\n");
  }

  if (!HTS.begin()) {
    error_reporter->Report("Failed to initialize humidity temperature sensor!");
    while (1);
  }
  // begin initialization
  if (!BLE.begin()) {
    error_reporter->Report("starting BLE failed!");
    while (1);
  }
    BLE.setLocalName("BatteryMonitor");
    BLE.setAdvertisedService(batteryService); // add the service UUID
    batteryService.addCharacteristic(batteryLevelChar); // add the battery level characteristic
    BLE.addService(batteryService); // Add the battery service
    batteryLevelChar.writeValue(oldBatteryLevel); // set initial value for this characteristic

    /* Start advertising BLE.  It will start continuously transmitting BLE
      advertising packets and will be visible to remote BLE central devices
      until it receives a new connection */

    // start advertising
    BLE.advertise();
    error_reporter->Report("Bluetooth device active, waiting for connections...");
}

void loop() {
  error_reporter->Report("\n----------------------------\nLoop.\n");
  // Don't try to clear the buffer again
  should_clear_buffer = false;

  BLEDevice central = BLE.central();
  if (central) {
    error_reporter->Report("Connected to central: ");
    // print the central's BT address:
    error_reporter->Report("%s", central.address());
    // turn on the LED to indicate the connection:
    digitalWrite(LED_BUILTIN, HIGH);

    // check the battery level every 200ms
    // while the central is connected:
    while (central.connected()) {
      long currentMillis = millis();
      // if 200ms have passed, check the battery level:
      if (currentMillis - previousMillis >= 200) {
        previousMillis = currentMillis;
        updateBatteryLevel();
      }
    }
  }

  // Perform a full scan / send cycle. The bool indicated whether the neural network
  // should be inferred from to reconfigure the operational parameters. 
  // This currently happens once a day.
  should_ask_nn = ThinkCycle(error_reporter, time_to_sleep);

  HandleOutput(error_reporter, time_to_sleep);
  
  error_reporter->Report("Should ask nn: %s", should_ask_nn ? "true" : "false" );
  delay(5000);                       // wait for a second
  error_reporter->Report("time_to_sleep: %d", time_to_sleep);
  delay(time_to_sleep);

  if (!should_ask_nn) return;
  
  error_reporter->Report("Asking neural network for updated config... (fake)");
  return;
  // Run inference, and report any error
  model_input->data.f[0] = 0.1;
  model_input->data.f[1] = -0.1;

  invoke_status = interpreter->Invoke();
  if (invoke_status != kTfLiteOk) {
    error_reporter->Report("Invoke failed.");
    error_reporter->Report("%s\n", invoke_status);
    return;
  }

  // Analyze the results to obtain a prediction
  error_reporter->Report("Interpreting NN output...");
  time_to_sleep = InterpretNNOutput(interpreter->output(0)->data.f);
  // Clear the buffer next time we read data
  should_clear_buffer = true;
  // Produce an output
  // HandleOutput(error_reporter, time_to_sleep);
}
