#include "main_functions.h"
#include "output_handler.h"
#include <Arduino_HTS221.h>  // Read sensors
#include <ArduinoBLE.h>
#include "think_cycle.h"
#include <stdlib.h>     /* rand */


// Globals, used for compatibility with Arduino-style sketches.
namespace {
  // ----------------------------- Sense Cycle Variables BEGIN -----------------------------
  bool should_clear_buffer = false;
  int time_to_sleep = 1000;
  bool should_ask_nn = false;

  // ------------------ Bluetooth ------------------
  BLEService batteryService("180F");
  BLEUnsignedCharCharacteristic batteryLevelChar("2A19", BLERead | BLENotify);
  int oldBatteryLevel = 0; 

  long start_timestamp;
  long end_timestamp;
  long total_diff;

  long start_ble_timestamp;
  long end_ble_timestamp;
  long ble_diff;
  // ----------------------------- Sense Cycle Variables END -----------------------------
}

void updateBatteryLevel() {
  int battery = analogRead(A0);
  int batteryLevel = map(battery, 0, 1023, 0, 100);

  Serial.print("Battery Level \% is now: ");
  Serial.println(batteryLevel); 
  batteryLevelChar.writeValue(batteryLevel);
  oldBatteryLevel = batteryLevel;

}

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // ----------------------------- Sense Cycle Setup BEGIN -----------------------------
  if (!HTS.begin()) {
    Serial.println("Failed to initialize humidity temperature sensor!");
    while (1);
  }
  // ------------------ Bluetooth ------------------
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");
    while (1);
  }

  BLE.setLocalName("BatteryMonitor");
  BLE.setAdvertisedService(batteryService);
  batteryService.addCharacteristic(batteryLevelChar);
  BLE.addService(batteryService);
  batteryLevelChar.writeValue(oldBatteryLevel);
  BLE.advertise();
  Serial.println("Bluetooth device active, waiting for connections...");
  // ----------------------------- Sense Cycle Variables END -----------------------------
}

void loop() {
  start_timestamp = millis();
  Serial.println("\n----------------------------\nLoop.\n");

  // ----------------------------- LOOP Step 1: Bluetooth -----------------------------
  start_ble_timestamp = millis();
  BLEDevice central = BLE.central();
  if (central) {
    Serial.print("Connected to BLE device: ");
    Serial.println(central.address());
    digitalWrite(LED_BUILTIN, HIGH);
    updateBatteryLevel();
  }
  end_ble_timestamp = millis();
  ble_diff = end_ble_timestamp - start_ble_timestamp;
  Serial.print(F("BLE time elapsed: "));
  Serial.println(ble_diff);
  
  // ----------------------------- LOOP Step 2: Perform Think Cycle -----------------------------
  should_ask_nn = ThinkCycle(time_to_sleep);


  // ----------------------------- LOOP Step 3: Ask NN if it's time -----------------------------
  // HandleOutput(time_to_sleep);
  // Serial.print("Should ask nn: ");
  // Serial.println(should_ask_nn ? "true" : "false");
  // if (should_ask_nn) {
  //   time_to_sleep = (rand() % 9 + 1) * 1000;
  //   time_to_sleep = 100;
  // }  

  // ----------------------------- LOOP Step 4: Sleep -----------------------------
  // Serial.print("time_to_sleep: ");
  // Serial.println(time_to_sleep);

  end_timestamp = millis();
  total_diff = end_timestamp - start_timestamp;
  Serial.print(F("Total time elapsed: "));
  Serial.println(total_diff);
  delay(time_to_sleep);
}
