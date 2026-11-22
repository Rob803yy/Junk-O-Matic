#pragma once
// DRAFT R0: no verified digital pin assignment exists. Defaults touch no sensor GPIO.
// Override with build flags for compilation tests; do not upload until pin/power review.
#ifndef ENABLE_IMU
#define ENABLE_IMU 0
#endif
#ifndef ENABLE_RANGE
#define ENABLE_RANGE 0
#endif
#ifndef ENABLE_FEEDBACK
#define ENABLE_FEEDBACK 0
#endif
#ifndef TRIG_PIN
#define TRIG_PIN -1
#endif
#ifndef ECHO_PIN
#define ECHO_PIN -1
#endif
#ifndef LED_PIN
#define LED_PIN -1
#endif
#ifndef BUZZER_PIN
#define BUZZER_PIN -1
#endif
#ifndef ALARM_DISTANCE_MM
#define ALARM_DISTANCE_MM -1
#endif
#define MPU_ADDRESS 0x68
#define SERIAL_BAUD 115200UL
#define SAMPLE_INTERVAL_MS 100UL
#define ECHO_TIMEOUT_US 25000UL
#define SOUND_MM_PER_US 0.343f  // Proposed room-temperature approximation; not calibrated.
#define FIRMWARE_ID "v2-r0"

static_assert(SAMPLE_INTERVAL_MS >= 60, "Keep ultrasonic retrigger interval >=60ms");
static_assert(!ENABLE_RANGE || (TRIG_PIN >= 2 && TRIG_PIN <= 13 && ECHO_PIN >= 2 && ECHO_PIN <= 13 && TRIG_PIN != ECHO_PIN), "Review and assign separate digital trigger/echo pins 2..13");
static_assert(!ENABLE_FEEDBACK || ENABLE_RANGE, "Distance feedback requires range acquisition");
static_assert(!ENABLE_FEEDBACK || (LED_PIN >= 2 && LED_PIN <= 13 && BUZZER_PIN >= 2 && BUZZER_PIN <= 13 && LED_PIN != BUZZER_PIN && ALARM_DISTANCE_MM > 0), "Review LED/buzzer driver, polarity and threshold");
static_assert(!ENABLE_FEEDBACK || (LED_PIN != TRIG_PIN && LED_PIN != ECHO_PIN && BUZZER_PIN != TRIG_PIN && BUZZER_PIN != ECHO_PIN), "Feedback pins overlap sensor pins");
