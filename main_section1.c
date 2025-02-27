// Important! DO NOT MODIFY this file.
// You will not submit this file.
// This file is provided for your understanding of the program procedure.

// Skeleton code of CSE237A, Sensor interaction
// For more details, please see the instructions on the class website.

#include <stdio.h>
#include <pthread.h>
#include <wiringPi.h>
#include <softPwm.h>
#include "assignment1.h"

// Thread declaration macros
#define thread_decl(NAME) \
void* thread_##NAME(void* param) { \
	SharedVariable* pV = (SharedVariable*) param; \
	body_##NAME(pV); \
	return NULL; }

// Declare threads for each sensor/actuator function
/*thread_decl(button)
thread_decl(motion)
thread_decl(sound)
thread_decl(encoder)
thread_decl(twocolor)
thread_decl(rgbcolor)
thread_decl(aled)
thread_decl(buzzer)*/
thread_decl(right)
thread_decl(left)
thread_decl(scroll)
thread_decl(pick)

// Thread creation and joining macros
#define thread_create(NAME) pthread_create(&t_##NAME, NULL, thread_##NAME, &v);
#define thread_join(NAME) pthread_join(t_##NAME, NULL);

int main(int argc, char* argv[]) {
	// Initialize shared variable
	SharedVariable v;

	// Initialize WiringPi library
	if (wiringPiSetup() == -1) {
		printf("Failed to setup wiringPi.\n");
		return 1; 
	}

	// Initialize shared variable and sensors
	init_shared_variable(&v);
	init_sensors(&v);

	// Thread identifiers
/*	pthread_t t_button,
			  t_motion,
			  t_sound,
			  t_encoder,
			  t_twocolor,
			  t_rgbcolor,
			  t_aled,
			  t_buzzer;*/
	pthread_t t_right, t_left, t_scroll, t_pick;

	// Main program loop
	while (v.bProgramExit != 1) {
		// Create sensing threads
	/*	thread_create(button);
		thread_create(motion);
		thread_create(sound);
		thread_create(encoder);
		thread_create(twocolor);
		thread_create(rgbcolor);
		thread_create(aled);
		thread_create(buzzer);*/
		thread_create(right);
		thread_create(left);
		thread_create(scroll);
		thread_create(pick);

		// Wait for all threads to finish
	/*	thread_join(button);
		thread_join(motion);
		thread_join(sound);
		thread_join(encoder);
		thread_join(twocolor);
		thread_join(rgbcolor);
		thread_join(aled);
		thread_join(buzzer);*/
		thread_join(right);
		thread_join(left);
		thread_join(scroll);
		thread_join(pick);

		// Add a slight delay between iterations
		delay(10);
	}

	printf("Program finished.\n");

	return 0;
}
