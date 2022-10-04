
#define RXD2 16
#define TXD2 17
//int voltage;
void setup() {
  
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);  // Note the format for setting a serial port (UART2) is as follows: Serial2.begin(baud-rate, protocol, RX pin, TX pin);
}

void loop() 
{
 
    String   voltageString = Serial2.readString();      // read and store the value of voltage sensor which recieved by UART2.
    int voltageInteger = voltageString.toInt();        // convert from string to integer.
    float voltageFloat= (float) voltageInteger/100;    // convert from integer to float and devided by 100 to get the real sensor value.
    //Serial.println(voltageString);
    Serial.println(voltageFloat);  
    delay(200);
    // say what you got:
    
   /* if (Serial2.available() > 0) {
      //Serial.print("I received: ");
      String   voltageRecieved = Serial2.readString();
      //voltage = Serial2.read();
      Serial.println(voltageRecieved);
    }
    int voltage = analogRead(Serial2.read());
    Serial.println(voltage);
    delay(200);
    /*  if (voltage > 155){
      Serial.println(voltage);
      //delay(200);
    }
    else if (voltage < 155 && voltage > 147) {
      Serial.println("I received:");
      delay(500);
      }
    Serial.println(voltage);
      delay(500);*/
   /* if (Serial1.available()) {      // If anything comes in Serial (USB),
    Serial.println(Serial1.read());   // read it and send it out Serial1 (pins 0 & 1)
  }*/
   /* Serial2.write(155);
    delay(500);*/
  }
