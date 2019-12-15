#include <Servo.h>

Servo servo1; // servo object to control

String str;

void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  servo1.attach(9); // attaches the servo to pin 9
  servo1.write(90);
  // put your setup code here, to run once:
}

void loop() {
  str = "";
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    str = Serial.readStringUntil('\n');
    Serial.flush();
    if (str == "unlock"){
      servo1.write(180);
    }
    else if (str == "lock"){
      servo1.write(90);
    }
    Serial.print(str);
  }

}
  // put your main code here, to run repeatedly:
