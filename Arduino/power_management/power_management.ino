#include "main_functions.h"
#include "toggle_led.h"
#include "SenseCycleOutput.h"

// ----------------------------- Sense Cycle Imports BEGIN -----------------------------
#include <Arduino_HTS221.h> // Read sensors
#include <ArduinoBLE.h>
#include "sense_cycle.h"
// ----------------------------- Sense Cycle Imports END -----------------------------

// ----------------------------- Tensorflow Lite Imports BEGIN -----------------------------

// Tensorflow model to use
#define STRINGIZE_EXPAND(A) #A
#define STRINGIZE(A) STRINGIZE_EXPAND(A)
// Default
// #define INCLUDEFILE murad_v1.h
// #define INCLUDEFILE ppo2_apr6.h
// #define MODEL ppo2_apr6_tflite
#define INCLUDEFILE src/dummy_networks/ppo2_dummy_4_128_8.h
#define MODEL ppo2_dummy_tflite
// Custom
#ifdef FILENAME
#define INCLUDEFILE FILENAME
// We assume MODELNAME is also defined if FILENAME is defined
#define MODEL MODELNAME
#endif
#include STRINGIZE(INCLUDEFILE)
// Tensorflow model end

#include <TensorFlowLite.h>

#include "tensorflow/lite/experimental/micro/kernels/micro_ops.h"
#include "tensorflow/lite/experimental/micro/micro_error_reporter.h"
#include "tensorflow/lite/experimental/micro/micro_interpreter.h"
#include "tensorflow/lite/experimental/micro/micro_mutable_op_resolver.h"
// #include "tensorflow/lite/experimental/micro/kernels/all_ops_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/version.h"
#include "interpret_nn_output.h"
// ----------------------------- Tensorflow Lite Imports END -----------------------------

// ---------------------------------------------------------------------------------------
//  Globals, used for compatibility with Arduino-style sketches.
// ---------------------------------------------------------------------------------------
namespace
{
// ----------------------------- Sense Cycle Variables BEGIN -----------------------------
int time_to_sleep = 1000;
bool should_ask_nn = false;

// ------------------ Bluetooth ------------------
BLEService batteryService("180F");
BLEUnsignedCharCharacteristic batteryLevelChar("2A19", BLERead | BLENotify);
BLEFloatCharacteristic tempChar("2A20", BLERead | BLENotify);

int oldBatteryLevel = 0;
// ----------------------------- Sense Cycle Variables END -----------------------------

// ----------------------------- Tensorflow Lite Variables START -----------------------------
tflite::ErrorReporter *error_reporter = nullptr;
const tflite::Model *model = nullptr;
tflite::MicroInterpreter *interpreter = nullptr;
TfLiteTensor *model_input = nullptr;
int input_length;
constexpr int kTensorArenaSize = 60 * 1024;
uint8_t tensor_arena[kTensorArenaSize];
TfLiteStatus invoke_status;

float input_1;
float input_2;
bool rising;

long before_invoke;
long after_invoke;
long invoke_diff;
long start_timestamp;
long end_timestamp;
long total_diff;
long start_cycle_timestamp;
long end_cycle_timestamp;
long cycle_diff;
long start_ble_timestamp;
long end_ble_timestamp;
long ble_diff;
long start_invoke_timestamp;
long end_invoke_timestamp;
long total_invoke_diff;

SenseCycleOutput sense_cycle_output;
// ----------------------------- Tensorflow Lite Variables END -----------------------------
} // namespace

void sendBluetoothData(SenseCycleOutput currentData)
{
  int battery = analogRead(A0);
  int batteryLevel = map(battery, 0, 1023, 0, 100);

  Serial.print(F("Battery Level \% is now: "));
  Serial.println(batteryLevel);
  batteryLevelChar.writeValue(batteryLevel);
  oldBatteryLevel = batteryLevel;

  float temp = currentData.temp;
  tempChar.writeValue(temp);
}

// ---------------------------------------------------------------------------------------
//  Setup
// ---------------------------------------------------------------------------------------
void setup()
{
  Serial.begin(9600);
  while (!Serial)
    ;

  // ----------------------------- Sense Cycle Setup BEGIN -----------------------------

  if (!HTS.begin())
  {
    Serial.println(F("Failed to initialize humidity temperature sensor!"));
    while (1)
      ;
  }
  // ------------------ Bluetooth ------------------
  if (!BLE.begin())
  {
    Serial.println(F("starting BLE failed!"));
    while (1)
      ;
  }

  BLE.setLocalName("PowerManagement");
  BLE.setAdvertisedService(batteryService);
  batteryService.addCharacteristic(batteryLevelChar);
  batteryService.addCharacteristic(tempChar);
  BLE.addService(batteryService);
  batteryLevelChar.writeValue(oldBatteryLevel);
  batteryLevelChar.writeValue((float)0.0);
  BLE.advertise();
  Serial.println(F("Bluetooth device active, waiting for connections..."));
  // ----------------------------- Sense Cycle Setup END -----------------------------

  // ----------------------------- Tensorflow Lite Setup START -----------------------------
  static tflite::MicroErrorReporter micro_error_reporter; // NOLINT
  error_reporter = &micro_error_reporter;
  model = tflite::GetModel(MODEL);
  if (model->version() != TFLITE_SCHEMA_VERSION)
  {
    Serial.println(F("Model provided is schema version not equal to supported version."));
    // model->version(), TFLITE_SCHEMA_VERSION);
    return;
  }

  // static tflite::ops::micro::AllOpsResolver all_ops_resolver;
  static tflite::MicroMutableOpResolver micro_mutable_op_resolver;
  micro_mutable_op_resolver.AddBuiltin(
      tflite::BuiltinOperator_FULLY_CONNECTED,
      tflite::ops::micro::Register_FULLY_CONNECTED());
  micro_mutable_op_resolver.AddBuiltin(
      tflite::BuiltinOperator_RELU,
      tflite::ops::micro::Register_RELU());

  static tflite::MicroInterpreter static_interpreter(
      model, micro_mutable_op_resolver, tensor_arena, kTensorArenaSize,
      error_reporter);
  interpreter = &static_interpreter;
  interpreter->AllocateTensors();

  input_1 = -1.0;
  input_2 = -1.0;
  rising = true;

  model_input = interpreter->input(0);

  Serial.print(F("Dims size"));
  Serial.println(model_input->dims->size);
  Serial.print(F("model_input->dims->data[0]"));
  Serial.println(model_input->dims->data[0]);
  Serial.print(F("model_input->dims->data[1]"));
  Serial.println(model_input->dims->data[1]);
  if ((model_input->dims->size != 2) ||
      (model_input->dims->data[0] != 1) || // Num outputs?
      (model_input->dims->data[1] != 4) || // Num inputs?
      (model_input->type != kTfLiteFloat32))
  {
    Serial.println(F("Bad input tensor parameters in model"));
  }
  input_length = model_input->bytes / sizeof(float);

  // ----------------------------- Tensorflow Lite Setup  END -----------------------------
}

// ---------------------------------------------------------------------------------------
//  Loop
// ---------------------------------------------------------------------------------------
void loop()
{
  start_timestamp = millis();
  Serial.println("<Arduino is ready>");
  Serial.println(F("\n----------------------------\nLoop.\n"));
  ToggleLed();

  // ----------------------------- LOOP Step 1: Perform Sense Cycle -----------------------------

  start_cycle_timestamp = millis();
  Serial.println(F("Performing sense cycle..."));
  sense_cycle_output = SenseCycle();
  Serial.print(F("sense_cycle_output temp: "));
  Serial.println(sense_cycle_output.temp);
  Serial.print(F("sense_cycle_output humidity: "));
  Serial.println(sense_cycle_output.humidity);
  Serial.print(F("sense_cycle_output should_ask_nn: "));
  Serial.println(sense_cycle_output.should_ask_nn);
  should_ask_nn = sense_cycle_output.should_ask_nn;

  end_cycle_timestamp = millis();
  cycle_diff = end_cycle_timestamp - start_cycle_timestamp;
  Serial.print(F("Cycle time elapsed: "));
  Serial.println(cycle_diff);

  // ----------------------------- LOOP Step 2: Send data -----------------------------
  start_ble_timestamp = millis();
  BLEDevice central = BLE.central();
  if (central)
  {
    Serial.print(F("\nConnected to BLE device: "));
    Serial.println(central.address());
    sendBluetoothData(sense_cycle_output);
  }

  end_ble_timestamp = millis();
  ble_diff = end_ble_timestamp - start_ble_timestamp;
  Serial.print(F("BLE time elapsed: "));
  Serial.println(ble_diff);

  // ----------------------------- LOOP Step 3: Ask NN (potentially) -----------------------------

  Serial.print(F("\nShould ask nn: "));
  Serial.println(F(should_ask_nn ? "true" : "false"));

  if (should_ask_nn)
  {
    // ----------------------------- Tensorflow Lite START -----------------------------
    start_invoke_timestamp = millis();
    Serial.println(F("Asking neural network for updated config..."));
    // TODO real NN input?
    input_1 = (rand() % 20) / 10.0 - 1.0;
    Serial.print(F("Input 1: "));
    Serial.println(input_1);
    input_2 = (rand() % 20) / 10.0 - 1.0;
    Serial.print(F("Input 2: "));
    Serial.println(input_2);

    model_input->data.f[0] = input_1;
    model_input->data.f[1] = input_2;
    model_input->data.f[2] = input_1;
    model_input->data.f[3] = input_2;

    Serial.println(F("After input setting."));

    before_invoke = millis();
    invoke_status = interpreter->Invoke();
    after_invoke = millis();
    invoke_diff = after_invoke - before_invoke;
    Serial.print(F("After invoke. Time spent:"));
    Serial.println(invoke_diff);

    if (invoke_status != kTfLiteOk)
    {
      Serial.print(F("Invoke failed: "));
      Serial.println(invoke_status);
      return;
    }

    Serial.print(F("Got NN Output! "));
    Serial.println(interpreter->output(0)->data.f[0]);

    Serial.print(F("Interpreting NN output..."));
    time_to_sleep = InterpretNNOutput(interpreter->output(0)->data.f);

    end_invoke_timestamp = millis();
    total_invoke_diff = end_invoke_timestamp - start_invoke_timestamp;
    Serial.print(F("Total invoke time elapsed: "));
    Serial.println(total_invoke_diff);
    // ----------------------------- Tensorflow Lite END -----------------------------
  }

  // ----------------------------- LOOP Step 4: Sleep -----------------------------
  Serial.print(F("time_to_sleep: "));
  Serial.println(time_to_sleep);
  ToggleLed();

  end_timestamp = millis();
  total_diff = end_timestamp - start_timestamp;
  Serial.print(F("Total time spent: "));
  Serial.println(total_diff);

  delay(time_to_sleep);
}
