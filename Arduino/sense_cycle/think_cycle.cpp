#include "think_cycle.h"
#include <time.h>       /* time_t, struct tm, difftime, time, mktime */
#include "Arduino.h"
#include <Arduino_HTS221.h>


// Globals, used for compatibility with Arduino-style sketches.
namespace {
  // The last time the neural network was asked for a config update
  // time_t last_config_update = time_t(0);
  // time_t timestamp;
  long last_config_update = millis();
  long timestamp;
  int seconds_since_last_check;
  bool should_ask_nn;

  long start_scan_timestamp;
  long end_scan_timestamp;
  long scan_diff;

  long start_timestamp;
  long end_timestamp;
  long total_diff;
  // double temperature;
  // double humidity;
}  // namespace


// Return the result of the last decision
// output is duty cycle, which we implement as some time to sleep (seconds)
bool ThinkCycle(int time_to_sleep) {
  start_timestamp = millis();
  // Serial.println("Initializing think cycle...\n");
  // Serial.print("last_config_update: ");
  // Serial.println(last_config_update);

  // TODO Perform some scan
   // read all the sensor values
  start_scan_timestamp = millis();
  float temperature = HTS.readTemperature();
  float humidity    = HTS.readHumidity();
  end_scan_timestamp = millis();
  scan_diff = end_scan_timestamp - start_scan_timestamp;
  Serial.print(F("Scan time elapsed: "));
  Serial.println(scan_diff);
  // Serial.println(" °C");
  // Serial.print("Humidity    = ");
  // Serial.print(humidity);
  // Serial.println(" %");


  // TODO Send scan results

  // Decide whether the Neural Network should be asked again to reconfigure 
  // operational parameters. For now we do this once a day.
  timestamp = millis();
  // Serial.print("timestamp: ");
  // Serial.println(timestamp);
  seconds_since_last_check = (int) (timestamp - last_config_update) / 1000;
  // Serial.print("seconds_since_last_check: ");
  // Serial.println((int) seconds_since_last_check);
  should_ask_nn = seconds_since_last_check > 10.0;  // 1 day

  if (should_ask_nn) {
    last_config_update = timestamp;
  }
  end_timestamp = millis();
  total_diff = end_timestamp - start_timestamp;
  Serial.print(F("Cycle time elapsed: "));
  Serial.println(total_diff);
  return should_ask_nn;
}
