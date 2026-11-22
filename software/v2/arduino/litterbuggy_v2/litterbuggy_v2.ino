/* LitterBuggy V2 acquisition draft for owner-confirmed Elegoo Uno R3.
 * Proposed protocol; not recovered original firmware. No drive-control code.
 * Disabled/missing measurements are null, never synthetic sensor readings.
 */
#include <Arduino.h>
#include <Wire.h>
#include "config.h"

#if !defined(__AVR_ATmega328P__)
#error "Review target: Elegoo Uno R3 / ATmega328P"
#endif

enum Flags : uint8_t { IMU_DISABLED=1, IMU_FAULT=2, RANGE_DISABLED=4, RANGE_TIMEOUT=8 };
uint32_t sequenceNumber=0, lastSample=0, lastImuRetry=0;
bool imuReady=false;

bool readRegisters(uint8_t reg, uint8_t *data, uint8_t count) {
  Wire.clearWireTimeoutFlag();
  Wire.beginTransmission(MPU_ADDRESS); Wire.write(reg);
  if (Wire.endTransmission(false) != 0) return false;
  const uint8_t received=Wire.requestFrom((uint8_t)MPU_ADDRESS,count,(uint8_t)true);
  if (received != count || Wire.getWireTimeoutFlag()) { while(Wire.available()) Wire.read(); return false; }
  for(uint8_t i=0;i<count;i++) data[i]=Wire.read();
  return true;
}
bool writeRegister(uint8_t reg,uint8_t value) {
  Wire.beginTransmission(MPU_ADDRESS);Wire.write(reg);Wire.write(value);
  return Wire.endTransmission(true)==0;
}
bool initialiseImu() {
  uint8_t who=0;
  if(!readRegisters(0x75,&who,1) || (who & 0x7e)!=0x68) return false;
  // PWR_MGMT_1, CONFIG(DLPF), SMPLRT_DIV, GYRO_CONFIG, ACCEL_CONFIG.
  return writeRegister(0x6b,0x01) && writeRegister(0x1a,0x03) &&
         writeRegister(0x19,9) && writeRegister(0x1b,0) && writeRegister(0x1c,0);
}
void setup() {
  Serial.begin(SERIAL_BAUD);
#if ENABLE_IMU
  Wire.begin();Wire.setClock(100000);Wire.setWireTimeout(25000,true);
  imuReady=initialiseImu();
#endif
#if ENABLE_RANGE
  pinMode(TRIG_PIN,OUTPUT);digitalWrite(TRIG_PIN,LOW);pinMode(ECHO_PIN,INPUT);
#endif
#if ENABLE_FEEDBACK
  pinMode(LED_PIN,OUTPUT);digitalWrite(LED_PIN,LOW);
  pinMode(BUZZER_PIN,OUTPUT);digitalWrite(BUZZER_PIN,LOW);
#endif
}
void loop() {
  const uint32_t now=millis();
  if((uint32_t)(now-lastSample)<SAMPLE_INTERVAL_MS) return;
  lastSample=now;uint8_t flags=0;int16_t imu[7];bool imuValid=false;
  uint32_t echo=0;uint16_t distance=0;
#if ENABLE_IMU
  if(!imuReady && (uint32_t)(now-lastImuRetry)>=2000) {
    lastImuRetry=now;imuReady=initialiseImu();
  }
  uint8_t bytes[14];
  if(imuReady && readRegisters(0x3b,bytes,14)) {
    for(uint8_t i=0;i<7;i++) imu[i]=(int16_t)((uint16_t)bytes[2*i]<<8 | bytes[2*i+1]);
    imuValid=true;
  } else {imuReady=false;flags|=IMU_FAULT;}
#else
  flags|=IMU_DISABLED;
#endif
#if ENABLE_RANGE
  digitalWrite(TRIG_PIN,LOW);delayMicroseconds(2);
  digitalWrite(TRIG_PIN,HIGH);delayMicroseconds(10);digitalWrite(TRIG_PIN,LOW);
  echo=pulseIn(ECHO_PIN,HIGH,ECHO_TIMEOUT_US);
  if(echo==0) flags|=RANGE_TIMEOUT;
  else distance=(uint16_t)(echo*SOUND_MM_PER_US/2.0f+0.5f);
#else
  flags|=RANGE_DISABLED;
#endif
#if ENABLE_FEEDBACK
  // Proposed local active-high LED and passive-buzzer behaviour; original thresholds unknown.
  const bool alarm=echo>0 && distance<ALARM_DISTANCE_MM;
  digitalWrite(LED_PIN,alarm?HIGH:LOW);
  if(alarm) tone(BUZZER_PIN,2000,40);else noTone(BUZZER_PIN);
#endif
  Serial.print(F("{\"v\":2,\"type\":\"telemetry\",\"fw\":\"" FIRMWARE_ID "\",\"seq\":"));
  Serial.print(sequenceNumber++);Serial.print(F(",\"ms\":"));Serial.print(now);
  Serial.print(F(",\"imu_raw\":"));
  if(imuValid) {Serial.print('[');for(uint8_t i=0;i<7;i++){if(i)Serial.print(',');Serial.print(imu[i]);}Serial.print(']');}
  else Serial.print(F("null"));
  Serial.print(F(",\"echo_us\":"));if(echo)Serial.print(echo);else Serial.print(F("null"));
  Serial.print(F(",\"distance_mm\":"));if(echo)Serial.print(distance);else Serial.print(F("null"));
  Serial.print(F(",\"flags\":"));Serial.print(flags);Serial.println('}');
}
