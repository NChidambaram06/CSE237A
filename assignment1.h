
#ifndef _ASSIGNMENT_BODY_
#define _ASSIGNMENT_BODY_

#include <stdint.h>

// Macros
#define TURN_ON(pin) digitalWrite(pin, 1)
#define TURN_OFF(pin) digitalWrite(pin, 0)

#define READ(pin) digitalRead(pin)
#define WRITE(pin, x) digitalWrite(pin, x)

// Constants
#define RUNNING 3
#define PAUSE 2

#define LOW 0
#define HIGH 1

#define CLOCKWISE 0
#define COUNTER_CLOCKWISE 1

#define DETECT_SOUND 1
#define NO_SOUND 0

// A. Pin number definitions (DO NOT MODIFY)
// We use 4 touch sensors.
//
// 1. Touch Sensors
#define PIN_LEFT 0
#define PIN_RIGHT 2
#define PIN_SCROLL 3
#define PIN_PICK 4


// B. Shared structure
// All thread functions get a shared variable of the structure
// as the function parameter.
// If needed, you can add anything in this structure.
typedef struct shared_variable {
    int bProgramExit; // Once set to 1, the program will terminate.
    // You can add more variables if needed.
    int right;
    int left;
    int scroll;
    int pick;
    int rightLastClickTime;
    int leftLastClickTime;
    int scrollLastClick;
    int pickLastClick;
} SharedVariable;

// C. Functions
// You need to implement the following functions.
// Do not change any function name here.
void init_shared_variable(SharedVariable* sv);
void init_sensors(SharedVariable* sv);/*
void body_button(SharedVariable* sv);     // Button
void body_motion(SharedVariable* sv);     // Infrared motion sensor
void body_sound(SharedVariable* sv);      // Microphone sound sensor
void body_encoder(SharedVariable* sv);    // Rotary encoder
void body_twocolor(SharedVariable* sv);   // DIP two-color LED
void body_rgbcolor(SharedVariable* sv);   // SMD RGB LED
void body_aled(SharedVariable* sv);       // Auto-flash LED
void body_buzzer(SharedVariable* sv);     // Buzzer*/
void body_right(SharedVariable* sv);
void body_left(SharedVariable* sv);
void body_scroll(SharedVariable* sv);
void body_pick(SharedVariable* sv);

#endif
