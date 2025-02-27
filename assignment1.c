#include "assignment1.h"
#include <stdio.h>
#include <wiringPi.h>
#include <softPwm.h>
#include <sys/time.h>

int getMillis() {
        struct timeval t;
        gettimeofday(&t, NULL);
        return (int)((t.tv_sec * 1000) + (t.tv_usec/1000));
}

void init_shared_variable(SharedVariable* sv) {
    sv->bProgramExit = 0;
// You can initialize the shared variable if needed.
    sv->right = 0;
    sv->left = 0;
    sv->scroll = 0;
    sv->pick = 1;
    sv->rightLastClickTime = getMillis();
    sv->leftLastClickTime = getMillis();
    sv->scrollLastClick = getMillis();
    sv->pickLastClick = getMillis();
}

/*void ledInit(void) {
    softPwmCreate(PIN_SMD_RED, 0, 0xff);
    softPwmCreate(PIN_SMD_GRN, 0, 0xff);
    softPwmCreate(PIN_SMD_BLU, 0, 0xff);
    pinMode(PIN_DIP_RED, OUTPUT);
    pinMode(PIN_DIP_GRN, OUTPUT);
//......
//initialize SMD and DIP
}*/

void init_sensors(SharedVariable* sv) {
// .......
    pinMode(PIN_RIGHT, INPUT);
    pinMode(PIN_LEFT, INPUT);
    pinMode(PIN_SCROLL, INPUT);
    pinMode(PIN_PICK, INPUT);
    
   // ledInit();
}

// 1. Button
void body_right(SharedVariable* sv) {
    if (sv->pick == 1) {
        int currTime = getMillis();
        if (digitalRead(PIN_RIGHT) == HIGH & (currTime - sv->rightLastClickTime) > 400) {
            printf("right click\n");
            sv->right = 1;
            sv->rightLastClickTime = getMillis();
        } else if ((currTime - sv->rightLastClickTime) > 400) {
            sv->right = 0;
        }
    }
}

void body_left(SharedVariable* sv) {
    if (sv->pick == 1) {
        int currTime = getMillis();
        if (digitalRead(PIN_LEFT) == HIGH && (currTime - sv->leftLastClickTime) > 400) {
            printf("left click\n");
            sv->left = 1;
            sv->leftLastClickTime = getMillis();
        } else if ((currTime - sv->leftLastClickTime) > 400) {
            sv->left = 0;
        }
    }
}

void body_scroll(SharedVariable* sv) {
    if (sv->pick == 1) {
        int currTime = getMillis();
        if (digitalRead(PIN_SCROLL) == HIGH && (currTime - sv->scrollLastClick) > 0) {
            printf("scroll click\n");
            sv->scroll = 1;
            sv->scrollLastClick = getMillis();
        } else if ((currTime - sv->scrollLastClick) > 0){
            if (sv->scroll == 1) {printf("stop scroll click\n");}
            sv->scroll = 0;
        }
    }
}

void body_pick(SharedVariable* sv) {
    int currTime = getMillis();
    if (digitalRead(PIN_PICK) == HIGH && (currTime - sv->pickLastClick) > 400) {
        if (sv->pick == 0) {
            printf("pick up mouse\n");
            sv->pick = 1;
            sv->pickLastClick = getMillis();
        } else if ((currTime - sv->pickLastClick) > 400){
            printf("drop mouse\n");
            sv->pick = 0;
            sv->pickLastClick = getMillis();
        }
    }
}
