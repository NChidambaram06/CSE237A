#include <wiringPi.h>
#include <stdio.h>
// 7-color LED
#define LEDPin 5
// button
#define ButtonPin 5
// 2-color LED
#define RedPin 5
#define GreenPin 4
// rotary encoder
#define CLKPin 27
#define DTPin 16
#define SWPin 15
// buzzer
#define BUZPin 5
// obstacle detector
#define SIGPin 5
// rgb smd LED
#define REDSMDPin 6
#define BLUESMDPin 4
#define GREENSMDPin 5
// microphone
#define MICPin 5

/* 7-color flashing LED
int main(void)
{
	if(wiringPiSetup() == -1){
		//if the wiringPi initialization fails, print error message
		printf("setup wiringPi failed !");
		return 1;
	}
	pinMode(LEDPin, OUTPUT);
	while(1){
		digitalWrite(LEDPin, LOW); //led off
		printf("led off...\n");
		delay(500);
		digitalWrite(LEDPin, HIGH); //led on
		printf("...led on\n");
		delay(500);
	}
	return 0;
}
*/

/* button 
int main(void)
{
	if(wiringPiSetup() == -1){
		//if the wiringPi initialization fails, print error message
		printf("setup wiringPi failed !");
		return 1;
	}
	
	pinMode(ButtonPin, INPUT);
	pullUpDnControl(ButtonPin, PUD_UP);
	
	while(1){
		if (digitalRead(ButtonPin) == LOW){ // if button pressed
		printf("button pushed...\n");
		} else { // if button released
		printf("...button released\n");
		}
	}
	return 0;
}
*/

/* 2-color LED 
int main(void)
{
	if(wiringPiSetup() == -1){
		//if the wiringPi initialization fails, print error message
		printf("setup wiringPi failed !");
		return 1;
	}
	pinMode(RedPin, OUTPUT);
	pinMode(GreenPin, OUTPUT);
	while(1){
		digitalWrite(RedPin, HIGH); //red light
		digitalWrite(GreenPin, LOW);
		printf("led off...\n");
		delay(500);
		digitalWrite(GreenPin, HIGH); //green light
		digitalWrite(RedPin, LOW);
		printf("...led on\n");
		delay(500);
	}
	return 0;
}
*/

/* rotary encoder 
int main(void)
{
	if(wiringPiSetup() == -1){
		//if the wiringPi initialization fails, print error message
		printf("setup wiringPi failed !");
		return 1;
	}
	pinMode(CLKPin, INPUT);
	pinMode(DTPin, INPUT);
	pinMode(SWPin, INPUT);
	pullUpDnControl(SWPin, PUD_UP);
	while(1){
		int clkState = digitalRead(CLKPin);
		int dtState = digitalRead(DTPin);
		int swState = digitalRead(SWPin);
		
		printf("CLK: %d, DT: %d, SW: %d\n", clkState, dtState, swState);
		
		delay(100);
	}
	return 0;
}
*/

/* Passive Buzzer 
int main(void)
{
	if(wiringPiSetup() == -1){
		//if the wiringPi initialization fails, print error message
		printf("setup wiringPi failed !");
		return 1;
	}
	pinMode(BUZPin, OUTPUT);
	while(1){
		digitalWrite(BUZPin, LOW); //led off
		printf("buzzer off...\n");
		delay(500);
		digitalWrite(BUZPin, HIGH); //led on
		printf("...buzzer on\n");
		delay(500);
	}
	return 0;
}
*/

/* Obstacle Detector 
int main(void)
{
	if(wiringPiSetup() == -1){
		//if the wiringPi initialization fails, print error message
		printf("setup wiringPi failed !");
		return 1;
	}
	pinMode(SIGPin, INPUT);
	while(1){
		if (digitalRead(SIGPin) == LOW) {
			printf("Obstacle detected...\n");
		} else {
			printf("... No Obstacle detected\n");
		}
		delay(100);
	}
	return 0;
}
*/

/* RGB SMD-LED
int main(void)
{
	if(wiringPiSetup() == -1){
		//if the wiringPi initialization fails, print error message
		printf("setup wiringPi failed !");
		return 1;
	}
	pinMode(REDSMDPin, OUTPUT);
	pinMode(BLUESMDPin, OUTPUT);
	pinMode(GREENSMDPin, OUTPUT);
	while(1){
		digitalWrite(REDSMDPin, HIGH);
		digitalWrite(BLUESMDPin, LOW);
		digitalWrite(GREENSMDPin, LOW);
		printf("Red on...\n");
		delay(500);
		
		digitalWrite(REDSMDPin, LOW);
		digitalWrite(BLUESMDPin, HIGH);
		digitalWrite(GREENSMDPin, LOW);
		printf("Blue on...\n");
		delay(500);
		
		digitalWrite(REDSMDPin, LOW);
		digitalWrite(BLUESMDPin, LOW);
		digitalWrite(GREENSMDPin, HIGH);
		printf("Green on...\n");
		delay(500);
		
		digitalWrite(REDSMDPin, HIGH);
		digitalWrite(BLUESMDPin, HIGH);
		digitalWrite(GREENSMDPin, HIGH);
		printf("White (all) on...\n");
		delay(500);
		
		digitalWrite(REDSMDPin, LOW);
		digitalWrite(BLUESMDPin, LOW);
		digitalWrite(GREENSMDPin, LOW);
		printf("All off...\n");
		delay(500);
	}
	return 0;
}
*/

/* Microphone Sound Sensor */
int main(void)
{
	if(wiringPiSetup() == -1){
		//if the wiringPi initialization fails, print error message
		printf("setup wiringPi failed !");
		return 1;
	}
	pinMode(MICPin, INPUT);
	while(1){
		int micVal = digitalRead(MICPin);
		
		printf("Mic value: %d\n", micVal);
		delay(500);
	}
	return 0;
}

