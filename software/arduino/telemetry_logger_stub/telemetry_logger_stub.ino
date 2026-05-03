/*
  Junk-O-Matic V1.0A telemetry logger stub.

  Observational telemetry only. This sketch must not command steering,
  throttle, ESC, arming, deadman, or vehicle motion.
*/

const unsigned long SAMPLE_INTERVAL_MS = 1000;
unsigned long lastSampleMs = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // Wait for USB serial on boards that need it.
  }
}

void loop() {
  const unsigned long nowMs = millis();
  if (nowMs - lastSampleMs < SAMPLE_INTERVAL_MS) {
    return;
  }
  lastSampleMs = nowMs;

  const float auxBatteryVoltage = 23.7; // TODO replace with calibrated voltage divider read.
  const float rail12v = 12.1;           // TODO replace with calibrated voltage divider read.
  const float rail5v = 5.05;            // TODO replace with calibrated voltage divider read.
  const float imuRollDeg = 1.2;         // TODO replace with IMU read.
  const float imuPitchDeg = -0.7;       // TODO replace with IMU read.
  const float imuYawDeg = 85.4;         // TODO replace with IMU read.
  const float enclosureTempC = 34.2;    // TODO replace with temperature sensor read.
  const bool estop = false;             // TODO replace with observational input if installed.
  const int faultCode = 0;

  Serial.print("{\"aux_battery_voltage\":");
  Serial.print(auxBatteryVoltage, 2);
  Serial.print(",\"rail_12v\":");
  Serial.print(rail12v, 2);
  Serial.print(",\"rail_5v\":");
  Serial.print(rail5v, 2);
  Serial.print(",\"imu_roll_deg\":");
  Serial.print(imuRollDeg, 2);
  Serial.print(",\"imu_pitch_deg\":");
  Serial.print(imuPitchDeg, 2);
  Serial.print(",\"imu_yaw_deg\":");
  Serial.print(imuYawDeg, 2);
  Serial.print(",\"enclosure_temp_c\":");
  Serial.print(enclosureTempC, 2);
  Serial.print(",\"estop\":");
  Serial.print(estop ? "true" : "false");
  Serial.print(",\"fault_code\":");
  Serial.print(faultCode);
  Serial.println("}");
}
