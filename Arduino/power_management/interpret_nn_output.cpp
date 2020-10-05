
// #include "Arduino.h"
#include "interpret_nn_output.h"

// How many times the most recent gesture has been matched in a row
int time_to_sleep = 1000;

// Return the result of the last decision
// output is duty cycle, which we implement as some time to sleep (seconds)
int InterpretNNOutput(float* output) {
  // Find whichever output has a probability > 0.8 (they sum to 1)
  
  // Serial.print("interpret param received:")
  // xSerial.println(output)
  // Time to sleep (ms)
  time_to_sleep = (int) ((*output + 1) * 5000.0); // Converts range [-1, 1] to [0, 10000]
  return time_to_sleep;
}
