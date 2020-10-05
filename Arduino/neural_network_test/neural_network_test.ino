
#include <TensorFlowLite.h>
// #include <MemoryBrute.h>

#include "main_functions.h"
#include <math.h>

// Tensorflow model to use
#define STRINGIZE_EXPAND(A) #A
#define STRINGIZE(A) STRINGIZE_EXPAND(A)
// Default
// #define INCLUDEFILE murad_v1.h
// #define INCLUDEFILE ppo2_apr6.h
// #define MODEL ppo2_apr6_tflite 
#define INCLUDEFILE src/dummy_networks/ppo2_dummy_2_1024_8.h
#define MODEL ppo2_dummy_tflite 
// Custom
#ifdef FILENAME
  #define INCLUDEFILE FILENAME
  // We assume MODELNAME is also defined if FILENAME is defined
  #define MODEL MODELNAME
#endif
#include STRINGIZE(INCLUDEFILE)
// Tensorflow model end

#include "tensorflow/lite/experimental/micro/kernels/micro_ops.h"
#include "tensorflow/lite/experimental/micro/micro_error_reporter.h"
#include "tensorflow/lite/experimental/micro/micro_interpreter.h"
#include "tensorflow/lite/experimental/micro/micro_mutable_op_resolver.h"
// #include "tensorflow/lite/experimental/micro/kernels/all_ops_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/version.h"


// Globals, used for compatibility with Arduino-style sketches.
namespace {
  
  // ----------------------------- Tensorflow Lite START -----------------------------
  tflite::ErrorReporter* error_reporter = nullptr;
  const tflite::Model* model = nullptr;
  tflite::MicroInterpreter* interpreter = nullptr;
  TfLiteTensor* model_input = nullptr;
  int input_length;
  constexpr int kTensorArenaSize = 60 * 1024;
  uint8_t tensor_arena[kTensorArenaSize];
  TfLiteStatus invoke_status;
  // ----------------------------- Tensorflow Lite END -----------------------------

  int input_num;
  int* iterators = new int[0];
  float* inputs = new float[0];
  float* inputs_to_try = new float[4];
  int k;
  int num_iterations;

}  // namespace


// The name of this function is important for Arduino compatibility.
void setup() {
  Serial.begin(9600);
  while (!Serial);
  
  // pinMode(LED_BUILTIN, OUTPUT);
  // Serial.print(F("Memory free at start of setup: "));
  // Serial.println(checkMemory());

  // ----------------------------- Tensorflow Lite START -----------------------------
  if (const char* env_p = std::getenv("ASD")) {
    Serial.print(F("env: "));
    Serial.println(env_p);
  }

  static tflite::MicroErrorReporter micro_error_reporter;  // NOLINT
  error_reporter = &micro_error_reporter;
  model = tflite::GetModel(MODEL);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    error_reporter->Report(
        "Model provided is schema version %d not equal "
        "to supported version %d.",
        model->version(), TFLITE_SCHEMA_VERSION);
    return;
  }

  // Serial.println(checkMemory());

  static tflite::MicroMutableOpResolver micro_mutable_op_resolver;  // NOLINT

  micro_mutable_op_resolver.AddBuiltin(
      tflite::BuiltinOperator_FULLY_CONNECTED,
      tflite::ops::micro::Register_FULLY_CONNECTED(), 1, 4);
  micro_mutable_op_resolver.AddBuiltin(
      tflite::BuiltinOperator_RELU,
      tflite::ops::micro::Register_RELU());
  static tflite::MicroInterpreter static_interpreter(
      model, micro_mutable_op_resolver, tensor_arena, kTensorArenaSize,
      error_reporter);
  interpreter = &static_interpreter;
  interpreter->AllocateTensors();

  model_input = interpreter->input(0);


  // Serial.print(F("model_input->dims->size: "));
  // Serial.println(model_input->dims->size);
  // Serial.print(F("model_input->dims->data[0]: "));
  // Serial.println(model_input->dims->data[0]);
  // Serial.print(F("model_input->dims->data[1]: "));
  // Serial.println(model_input->dims->data[1]);
  /*
  Serial.print(F("model_input->dims->data[2]: "));
  Serial.println(model_input->dims->data[2]);
  Serial.print(F("model_input->dims->data[3]: "));
  Serial.println(model_input->dims->data[3]);
  Serial.print(F("model_input->dims->data[4]: "));
  Serial.println(model_input->dims->data[4]);
  Serial.print(F("model_input->type: "));
  */
  Serial.println(model_input->type);
  if ((model_input->dims->size != 2) ||
      (model_input->dims->data[0] != 1) || // Output size? Num inputs?
      (model_input->dims->data[1] != 4) || // input size?
      (model_input->dims->data[2] != 1) || // Input size?
      (model_input->type != kTfLiteFloat32)) {
    Serial.println(F("Bad input tensor parameters in model"));

  }

  // input_length = model_input->bytes / sizeof(float);

  input_num = model_input->dims->data[1];
  int* iterators_hack = new int[input_num];
  float* inputs_hack = new float[input_num];
  delete[] iterators;
  delete[] inputs;
  iterators = iterators_hack;
  inputs = inputs_hack;

  for (int m = 0; m < input_num; m++) {
    iterators[m] = 0;
    inputs[m] = -1.0;
  }
  num_iterations = 4;


  /*
  Serial.print(F("input_length: "));
  Serial.println(input_length);
  */
  // ----------------------------- Tensorflow Lite END -----------------------------
}
void loop() {
  error_reporter->Report("\n<----------------------------\nLoop.\n>");

  if (inputs[0] == inputs[1] && inputs[0] == 1.0) {
    // Reset
    inputs[0] = -1.0;
    inputs[1] = -1.0;
  } else if (inputs[1] == 1.0) {
    inputs[0] += 1.0;
    inputs[1] = -1.0;
  } else {
    inputs[1] += 1.0;
  }

  for (int i = 2; i < input_num; i += 2) {
    inputs[i] = inputs[0];
    inputs[i + 1] = inputs[1];
  }
  
  // k = input_num - 1;
  // if (iterators[k] < num_iterations) {
  //   inputs[k] += 0.5;
  //   iterators[k] += 1;
  // } else {
  //   while (k >= 0) {
  //     if (iterators[k] >= num_iterations) {
  //       if (k == 0) {
  //         for (int m = 0; m < input_num; m++) {
  //           inputs[m] = -1.0;
  //           iterators[m] = 0;
  //         }
  //       } else {
  //         inputs[k] = -1.0;
  //         iterators[k] = 0;
  //         inputs[k - 1] += 0.5;
  //         iterators[k - 1] += 1;
  //       }
  //       k -= 1;
  //     } else { 
  //       k = -1;
  //     }
  //   }
  // }

  // ----------------------------- Tensorflow Lite START -----------------------------
  
  for (int m = 0; m < input_num; m++) {
    Serial.print(F("Input : "));
    Serial.print(m);
    Serial.print(F(": "));
    Serial.println(inputs[m]);
    model_input->data.f[m] = inputs[m];
  }

  error_reporter->Report("Asking neural network for updated config...");
  // Serial.print(F("Memory free just before invoke: "));
  // Serial.println(checkMemory());
  invoke_status = interpreter->Invoke();
  
  if (invoke_status != kTfLiteOk) {
    error_reporter->Report("Invoke failed.");
    return;
  }

  Serial.print(F("Invoke status: "));
  Serial.println(invoke_status);
  // Serial.print(F("Memory free just after invoke: "));
  // Serial.println(checkMemory());

  error_reporter->Report("Interpreting NN output...");
  Serial.println(interpreter->output(0)->data.f[0]);
  error_reporter->Report("output: %f", interpreter->output(0)->data.f[0]);
  // float* output = interpreter->output(0)->data.f;
  // Serial.println(*output);
  // error_reporter->Report("output: %s", interpreter->output(0)->data.f[0]);
  // Serial.println(interpreter->output(0)->data.f[0]);
  // ----------------------------- Tensorflow Lite END -----------------------------

  /*
  Serial.print(F("Memory free end of loop: "));
  Serial.println(checkMemory());

  */
  delay(100);
}
