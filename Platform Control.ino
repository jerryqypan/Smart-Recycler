#include <Servo.h>  
                                 
Servo TiltServo;                             // Declare left and right servos
int input = 2;                              //0 = trash, 1 = recycling, 2 = stationary
 
void setup()                                 // Built-in initialization block
{
  Serial.begin(9600);
  
  TiltServo.attach(13);                      // Attach left signal to pin 13
}  

void loop() { // run over and over
  if (Serial.available()>0){                // If something is available in the serial port
     input = Serial.read() - 48;            // Account for ascii
     if (input == 0) {
      //Serial.print("0");
      TiltServo.writeMicroseconds(1300);    // Tilt left then return to normal
      delay(1500);
      TiltServo.writeMicroseconds(1500);
     }
     if (input == 1) {
      //Serial.print("1");
      TiltServo.writeMicroseconds(1700);    // Tilt right then return to normal
      delay(1500);
      TiltServo.writeMicroseconds(1500);
     }
     input = 2;
  }
  delay(1500);
}
