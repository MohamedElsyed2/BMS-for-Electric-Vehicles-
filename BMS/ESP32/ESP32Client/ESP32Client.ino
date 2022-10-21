#include <cstring>
#include <iostream>
#include <stdlib.h>
#include <WiFi.h>
#include <PubSubClient.h>
//***************************************************//
//start of initialize the WiFi SSID and pasword
const char *ssid = "Elsyed";//"Familie";   // Enter your WiFi name
const char *password = "f83c1915";//"Mo&Em&Iy 93.95.20";  // Enter WiFi password
//End of initialize the WiFi SSID and pasword
//*************************************************//
//Start of initialize the MQTT broker, port, username and password
const char *mqtt_broker = "broker.emqx.io";
const char *mqtt_username = "emqx";
const char *mqtt_password = "public";
const int mqtt_port = 1883;
//End of initialize the MQTT broker, port, username and password
//*********************************************//
//initialize ESP32 client UART pins as GPIO 16,17
//#define RXD2 16
//#define TXD2 17
//********************************************//
WiFiClient espClient;
PubSubClient client(espClient);
//*********************************************//


void setup() {
  // Start of setup code
  //***************************************************//
 Serial.begin(115200);  // Set the Arduino serial monitor baud rate to 115200 
 //*****************************************************//
 //Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);   // the format for setting a serial port (UART2) is as follows: Serial2.begin(baud-rate, protocol, RX pin, TX pin);
//*****************************************************//

 //start of setup code to connect to a WiFi network
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.println("Connecting to WiFi..");
 }
 Serial.println("Connected to the WiFi network");
 //End of setup code to connect to a WiFi network
//*****************************************************//
 //Start of setup to connect to a mqtt broker
 client.setServer(mqtt_broker, mqtt_port);
 client.setCallback(callback);
 while (!client.connected()) {
     String client_id = "esp32-client-";
     client_id += String(WiFi.macAddress());
     Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
     if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
         Serial.println("Connected to the EMQX mqtt broker ");
     } else {
         Serial.print("failed with state ");
         Serial.print(client.state());
         delay(2000);
     }
 }
 //End of setup code to connect to a mqtt broker
 //****************************************************//
 client.subscribe("fan",0);    //Setup the ESP client to subscribe to the topic 'fan'.
 client.subscribe("SOC_of_cell1",0);    //Setup the ESP client to subscribe to the topic
 
}
//End of the set up code
//**********************************************************************************************//
// Start of the Callback function to recieve and print the message that was sent to the topics.

int fan_status;     // intialize a fan_status variable to get the fan status{0,1}.
int cell1_state_of_charge;

void callback(char *topic, byte *payload, unsigned int length) {
  String Topic = topic;
  if (Topic == "fan"){
     String message;
     for (int i = 0; i < length; i++) {
         message = message + (char) payload[i];  // convert *byte to string
 }
 fan_status = message.toInt();
 Serial.print("fan_status = ");
 Serial.println(fan_status);
 }
 else if (Topic == "SOC_of_cell1"){
     String message;
     for (int i = 0; i < length; i++) {
         message = message + (char) payload[i];  // convert *byte to string
 }
 cell1_state_of_charge = message.toInt();
 Serial.print("cell1_state_of_charge = ");
 Serial.println(cell1_state_of_charge);
 }

}
//  End of the Callback function to recieve and print the message that was sent to topic 'fan'
//********************************************************//
void loop() {
  //start of void loop
 client.loop();
 //******************************************************************//
      //String   string_sensor_reading = Serial2.readString();        // read and store the value of  sensor which recieved by UART2.
     //Serial.println(string_sensor_reading);  
 //******************************************************************//
//begin code for creating an ID for every sensor reading
     String string_sensor_reading = "a4.5";  // assigning value to string 
     
    int string_sensor_reading_length = string_sensor_reading.length();
    
    char char_sensor_reading [string_sensor_reading_length + 1];  // declaring character array with the length of the string voltage.

    strcpy(char_sensor_reading, string_sensor_reading.c_str());  // copying the contents of the string to char array.
 
    if (char_sensor_reading[0] == 'a')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell1_voltage= char_sensor_reading;
        client.publish("cell1_voltage",char_cell1_voltage);
        delay(1000);
    }
    else if (char_sensor_reading[0] == 'b')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell2_voltage= char_sensor_reading;
        client.publish("cell2_voltage",char_cell2_voltage);
        delay(1000);
    }
    else if (char_sensor_reading[0] == 'c')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell3_voltage= char_sensor_reading;
        client.publish("cell3_voltage",char_cell3_voltage);
        delay(1000);
    }
    else if (char_sensor_reading[0] == 'd')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell4_voltage= char_sensor_reading;
        client.publish("cell4_voltage",char_cell4_voltage);
        delay(1000);  
    }
    else if (char_sensor_reading[0] == 'e')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell5_voltage= char_sensor_reading;
        client.publish("cell5_voltage",char_cell5_voltage);
        delay(1000);
    }
    else if (char_sensor_reading[0] == 'f')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell6_voltage= char_sensor_reading;
        client.publish("cell6_voltage",char_cell6_voltage);
        delay(1000);
    }
    else if (char_sensor_reading[0] == 'g')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell7_voltage= char_sensor_reading;
        client.publish("cell7_voltage",char_cell7_voltage);
        delay(1000);
    }
    else if (char_sensor_reading[0] == 'h')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell8_voltage= char_sensor_reading;
        client.publish("cell8_voltage",char_cell8_voltage);
        delay(1000);
    }
    else if (char_sensor_reading[0] == 'i')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell1_current= char_sensor_reading;
        client.publish("cell1_current",char_cell1_current);
        delay(1000);
    }
    else if (char_sensor_reading[0] == 'j')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell2_current= char_sensor_reading;
        client.publish("cell2_current",char_cell2_current);
        delay(1000);
    }
    else if (char_sensor_reading[0] == 'k')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell3_current= char_sensor_reading;
        client.publish("cell3_current",char_cell3_current);
        delay(1000);
    }
    else if (char_sensor_reading[0] == 'm')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell4_current= char_sensor_reading;
        client.publish("cell4_current",char_cell4_current);
        delay(1000);
    }
    else if (char_sensor_reading[0] == 'n')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell5_current= char_sensor_reading;
        client.publish("cell5_current",char_cell5_current);
        delay(1000);
    }
    else if (char_sensor_reading[0] == 'p')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell6_current= char_sensor_reading;
        client.publish("cell6_current",char_cell6_current);
        delay(1000);
    }
    else if (char_sensor_reading[0] == 'q')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell7_current= char_sensor_reading;
        client.publish("cell7_current",char_cell7_current);
        delay(1000);
    }
    else if (char_sensor_reading[0] == 'r')   //check the ID of thery sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_cell8_current= char_sensor_reading;
        client.publish("cell8_current",char_cell8_current);
        delay(1000);
    }
    else if (char_sensor_reading[0] == 't')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]=' ';
        char *char_battery_temperature= char_sensor_reading;
        client.publish("battery_temperature",char_battery_temperature);
        delay(1000);
    }

//End code for creating an ID for every sensor readin
/*******************************************************/


 
 //char *char_temperature= "30.5";  // define the temperature be published as char, because the UART return string.
 //client.publish("battery_temperature",char_temperature);
 //delay(1000);
 //client.publish("battery_temperature", "40.05");
 //delay(500);
 //End the code to publish the battery temperature
 //*************************************************//
}
//End of void loop
