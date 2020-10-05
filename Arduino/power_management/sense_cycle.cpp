
#include "sense_cycle.h"
//#include <time.h>      
#include "Arduino.h"
#include <Arduino_HTS221.h>
#include "SenseCycleOutput.h"


// Globals, used for compatibility with Arduino-style sketches.
namespace {
  // The last time the neural network was asked for a config update
  // time_t last_config_update = time_t(0);
  // time_t timestamp;
  long last_config_update = millis();

  long timestamp;
  int seconds_since_last_check;
  bool should_ask_nn;
  float temperature;
  float humidity;

}  // namespace

// Return the result of the last decision
// output is duty cycle, which we implement as some time to sleep (seconds)
SenseCycleOutput SenseCycle() {
  long timestamp;
  int seconds_since_last_check;
  bool should_ask_nn;
  float temperature;
  float humidity;
  // Serial.println(F("Initializing sense cycle...\n"));
  // Serial.print(F("last_config_update: "));
  // Serial.println(last_config_update);

   // read all the sensor values
  temperature = HTS.readTemperature();
  // temperature = 20.0;
  humidity    = HTS.readHumidity();
  // humidity    = 30.0;
  // Serial.print(F("Temperature = "));
  // Serial.print(temperature);
  // Serial.println(F(" °C"));
  // Serial.print(F("Humidity    = "));
  // Serial.print(humidity);
  // Serial.println(F(" %"));

  // TODO Send scan results

  // Decide whether the Neural Network should be asked again to reconfigure 
  // operational parameters. For now we do this once a day.
  timestamp = millis();
  seconds_since_last_check = (int) (timestamp - last_config_update) / 1000;
  // Serial.print(F("seconds_since_last_check: "));
  // Serial.println((int) seconds_since_last_check);
  should_ask_nn = seconds_since_last_check > 10.0;  // 1 day?

  if (should_ask_nn) {
    last_config_update = timestamp;
  }

  SenseCycleOutput output;
  output.temp = temperature;
  output.humidity = humidity;
  output.should_ask_nn = should_ask_nn;

  return output;
}
