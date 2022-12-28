
#include <iostream>
#include <string> 
#include <stdlib.h>

#include <WiFi.h>
#include <PubSubClient.h>

//***************************************************//
//start of initialize the WiFi SSID and pasword
//const char *ssid = "Elsyed";                                   // Enter your WiFi name
//const char *password = "f83c1915";       // Enter WiFi password

const char *ssid = "Familie";
const char *password = "Mo&Em&Iy 93.95.20";               // Enter WiFi password
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
#define RXD2 16
#define TXD2 17
//********************************************//
WiFiClient espClient;
PubSubClient client(espClient);
//*********************************************//


void setup() {
  // Start of setup code
  //***************************************************//
 Serial.begin(115200);  // Set the Arduino serial monitor baud rate to 115200 
 //*****************************************************//
 Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);   // the format for setting a serial port (UART2) is as follows: Serial2.begin(baud-rate, protocol, RX pin, TX pin);
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
 client.subscribe("soc_cell1",1);    //Setup the ESP client to subscribe to the topic
 client.subscribe("errors",1);    
 client.subscribe("SOH_cell1",1);
 
}
//End of the set up code
//**********************************************************************************************//
// Start of the Callback function to recieve and print the message that was sent to the topics.

int fan_status;     // intialize a fan_status variable to get the fan status{0,1}.
float cell1_state_of_charge;

void callback(char *topic, byte *payload, unsigned int length) {
  if (strcmp(topic, "fan") == 0){
     String message;
     for (int i = 0; i < length; i++) {
         message = message + (char) payload[i];  // convert *byte to string
 }
 fan_status = message.toInt();
 Serial.print("fan_status = ");
 Serial.println(fan_status);
 }

 //************ Read the message recieved on topic "soc_cell1"***************//
  if (strcmp(topic, "soc_cell1") == 0){
     String message;
     for (int i = 0; i < length; i++) {
         message = message + (char) payload[i];         // convert *byte to string
 }

 cell1_state_of_charge = message.toFloat();
 Serial.print("cell1_state_of_charge = ");
 Serial.println(cell1_state_of_charge);
 //int soc = (int)(cell1_state_of_charge*100);
 //String soc_string = String(soc);
 //Serial.println(soc_string);
 //char* soc_char = (char*) malloc(sizeof(char)*soc_string.length()+1);
 //soc_string.toCharArray(soc_char, soc_string.length()+1);
 char txdata [6];
 sprintf(txdata,"%c%.2f",'s',cell1_state_of_charge);
 Serial2.write(txdata);
 //free(soc_char);
 }

 //***************************************************************//
 //************ Read the message recieved on topic "soc_cell1"***************//
  if (strcmp(topic, "SOH_cell1") == 0){
     String message;
     for (int i = 0; i < length; i++) {
         message = message + (char) payload[i];         // convert *byte to string
 }

 int cell1_state_of_health = message.toInt();
 Serial.print("cell1_state_of_health = ");
 Serial.println(cell1_state_of_health);

 char txdata [6];
 sprintf(txdata,"%c%d",'h',cell1_state_of_health); 
 Serial2.write(txdata);
 }

 //***************************************************************//
 if (strcmp(topic, "errors") == 0)
 {
     String message;
     for (int i = 0; i < length; i++) {
         message = message + (char) payload[i];  // convert *byte to string.
 }
 int error = message.toInt();
 switch (error){            // if error=1 means the sensors are not connected.
   case 5 :
   {
     char txdata [6];
     sprintf(txdata,"%c%d",'e',00005);
     Serial2.write(txdata);
   }
  
 }
 }
}
//****//  End of the Callback function to recieve messages.********************//

//********************************************************//
void loop() {
  //start of void loop
 client.loop();
 //*********************************************************//
 
//callback_func();

 //************** read and store the value of  sensor which recieved by UART2.**********************//
 if (Serial2.available()) {
      String   string_sensor_reading = Serial2.readString();        
      Serial.println(string_sensor_reading);

    int string_sensor_reading_length = string_sensor_reading.length();     //begin code for creating an ID for every sensor reading 
    
    char char_sensor_reading [string_sensor_reading_length + 1];  // declaring character array with the length of the string voltage.

    strcpy(char_sensor_reading, string_sensor_reading.c_str());  // copying the contents of the string to char array.

    switch (char_sensor_reading[0]) {   //check the ID of the sensor reading, then convert it to the true value without the ID (the ID is the frist char).
        case 'a':
            {
            char_sensor_reading[0]=' ';
            char *char_cell1_voltage= char_sensor_reading;
            client.publish("cell1_voltage",char_cell1_voltage);
           
            }
            break;
        case 'b':
            {
            char_sensor_reading[0]=' ';
            char *char_cell2_voltage= char_sensor_reading;
            client.publish("cell2_voltage",char_cell2_voltage);
            //delay(1000);
            }
            break;
        case 'c':
            {
            char_sensor_reading[0]=' ';
            char *char_cell3_voltage= char_sensor_reading;
            client.publish("cell3_voltage",char_cell3_voltage);
            //delay(1000);
            }
            break;
        
        case 'd':
            {
            char_sensor_reading[0]=' ';
            char *char_cell4_voltage= char_sensor_reading;
            client.publish("cell4_voltage",char_cell4_voltage);
            //delay(1000);
            }
            break;
        case 'i':
            {
            char_sensor_reading[0]=' ';
            char *char_cell1_current= char_sensor_reading;
            client.publish("cell1_current",char_cell1_current);
            //delay(1000);
            }
            break;
        case 'g':
            {
            char_sensor_reading[0]=' ';
            char *char_cell2_current= char_sensor_reading;
            client.publish("cell2_current",char_cell2_current);
            //delay(1000);
            }
            break;
        case 'h':
            {
            char_sensor_reading[0]=' ';
            char *char_cell3_current= char_sensor_reading;
            client.publish("cell3_current",char_cell3_current);
            //delay(1000);
            }
            break;
        case 'k':
            {
            char_sensor_reading[0]=' ';
            char *char_cell4_current= char_sensor_reading;
            client.publish("cell4_current",char_cell4_current);
            //delay(1000);
            }
            break;
        case 't':
            {
            char_sensor_reading[0]=' ';
            char *char_battery_temperature= char_sensor_reading;
            client.publish("battery_temperature",char_battery_temperature);
            //delay(1000);
            }
            break;
        
       default:
            // if frist charackter doesn't match any case )
           
            client.publish("sensors_Error","1");
            break;
    
//End code for creating an ID for every sensor readin
//*******************************************************
}

}

 //*******************End of if avilable code*****************************
}
//End of void loop
