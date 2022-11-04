/*
  Multiple Serial test

  Receives from the main serial port, sends to the others.
  Receives from serial port 1, sends to the main serial (Serial 0).

  This example works only with boards with more than one serial like Arduino Mega, Due, Zero etc.

  The circuit:
  - any serial device attached to Serial port 1
  - Serial Monitor open on Serial port 0

  created 30 Dec 2008
  modified 20 May 2012
  by Tom Igoe & Jed Roach
  modified 27 Nov 2015
  by Arturo Guadalupi

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/MultiSerialMega
*/


#define RXD2 16
#define TXD2 17


void setup() {
  
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);  // Note the format for setting a serial port (UART2) is as follows: Serial2.begin(baud-rate, protocol, RX pin, TX pin);
}

void loop() {
  // read from port 1, send to port 0:
  if (Serial2.available()) {
    String inByte = Serial2.readString();
    Serial.println(inByte);
    //delay(2000);
    }

}
