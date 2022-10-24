
#include <cstring>
#include <iostream>
#include <stdlib.h>
using namespace std;

#define RXD2 16
#define TXD2 17


void setup() {
  
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);  // Note the format for setting a serial port (UART2) is as follows: Serial2.begin(baud-rate, protocol, RX pin, TX pin);
}

void loop() 
{
 
     /*************************************************************************************************************************************/
     if (Serial2.available()) {
     String   string_sensor_reading = Serial2.readString();        // read and store the value of  sensor which recieved by UART2.
     Serial.println(string_sensor_reading);  
     
    int string_sensor_reading_length = string_sensor_reading.length();
    
    char char_sensor_reading [string_sensor_reading_length + 1];  // declaring character array with the length of the string voltage.

    strcpy(char_sensor_reading, string_sensor_reading.c_str());  // copying the contents of the string to char array.
 
    if (char_sensor_reading[0] == 'a')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        int cell1_int_voltage =  atoi ( char_sensor_reading);  // convert char array  to integer
        Serial.println(cell1_int_voltage);  // print the value to be published later.
    }
    else if (char_sensor_reading[0] == 'b')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        int cell2_int_voltage =  atoi ( char_sensor_reading);  // convert char array  to integer
        Serial.println(cell2_int_voltage);
    }
    else if (char_sensor_reading[0] == 'c')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        int cell3_int_voltage =  atoi ( char_sensor_reading);  // convert char array to integer
        Serial.println(cell3_int_voltage);
    }
    else if (char_sensor_reading[0] == 'd')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell4_int_voltage =  atoi ( char_sensor_reading);  // convert char array  to integer
        Serial.println(cell4_int_voltage);  
    }
    else if (char_sensor_reading[0] == 'e')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell5_int_voltage =  atoi ( char_sensor_reading);  // convert char array to integer
        Serial.println(cell5_int_voltage);
    }
    else if (char_sensor_reading[0] == 'f')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell6_int_voltage =  atoi ( char_sensor_reading);  // convert char array to integer
        Serial.println(cell6_int_voltage);
    }
    else if (char_sensor_reading[0] == 'g')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell7_int_voltage =  atoi ( char_sensor_reading);  // convert char array to integer
        Serial.println(cell7_int_voltage);
    }
    else if (char_sensor_reading[0] == 'h')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell8_int_voltage =  atoi ( char_sensor_reading);  // convert char array to integer
        Serial.println(cell8_int_voltage);
    }
    else if (char_sensor_reading[0] == 'i')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell1_int_current =  atoi ( char_sensor_reading);  // convert char array to integer
        Serial.println(cell1_int_current);
    }
    else if (char_sensor_reading[0] == 'j')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell2_int_current =  atoi ( char_sensor_reading);  // convert char array to integer
        Serial.println(cell2_int_current);
    }
    else if (char_sensor_reading[0] == 'k')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell3_int_current =  atoi ( char_sensor_reading);  // convert char array to integer
        Serial.println(cell3_int_current);
    }
    else if (char_sensor_reading[0] == 'm')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell4_int_current =  atoi ( char_sensor_reading);  // convert char array to integer
        Serial.println(cell4_int_current);
    }
    else if (char_sensor_reading[0] == 'n')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell5_int_current =  atoi ( char_sensor_reading);  // convert char array to integer
        Serial.println(cell5_int_current);
    }
    else if (char_sensor_reading[0] == 'p')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell6_int_current =  atoi ( char_sensor_reading);  // convert char array to integer
        Serial.println(cell6_int_current);
    }
    else if (char_sensor_reading[0] == 'q')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell7_int_current =  atoi ( char_sensor_reading);  // convert char array to integer
        Serial.println(cell7_int_current);
    }
    else if (char_sensor_reading[0] == 'r')   //check the ID of thery sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell8_int_current =  atoi ( char_sensor_reading);  // convert char array to integer
        Serial.println(cell8_int_current);
    }
    else if (char_sensor_reading[0] == 't')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int temperature_sensor =  atoi ( char_sensor_reading);  // convert char array to integer
        Serial.println(temperature_sensor);
    }

//End code for creating an ID for every sensor readin
//delay(1000);
}
}
    /* say what you got:
    //int voltageInteger = voltageString.toInt();           // convert from string to integer.
     //float voltageFloat= (float)voltageInteger/100; 
     //Serial.println(voltageFloat);// convert from integer to float and devided by 100 to get the real sensor value.
      //begin code for creating an ID for every sensor reading
     //String string_sensor_reading = "a148";  // assigning value to string 
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
