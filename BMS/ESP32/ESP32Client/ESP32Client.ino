#include <WiFi.h>
#include <PubSubClient.h>
//***************************************************//
//start of initialize the WiFi SSID and pasword
const char *ssid = "Familie";   // Enter your WiFi name
const char *password = "Mo&Em&Iy 93.95.20";  // Enter WiFi password
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
         Serial.println("Public emqx mqtt broker connected");
     } else {
         Serial.print("failed with state ");
         Serial.print(client.state());
         delay(2000);
     }
 }
 //End of setup code to connect to a mqtt broker
 //****************************************************//
 client.subscribe("fan");    //Setup the ESP client to subscribe to the topic
 
}
//End of the set up code
//**********************************************************************************************//
// Start of the Callback function to recieve and print the message that was sent to topic 'fan'
int fan_status;     // intialize a fan_status variable to get the fan status{0,1}
const char *topic = "fan";
void callback(char *topic, byte *payload, unsigned int length) {
 Serial.print("Message arrived in topic: ");
 Serial.println(topic);
 Serial.print("Message:");
 String message;
 for (int i = 0; i < length; i++) {
     message = message + (char) payload[i];  // convert *byte to string
 }
 Serial.print(message);
 fan_status = message.toInt();
 //if (message == "on") { digitalWrite(LED, LOW); }   // LED on
 //if (message == "off") { digitalWrite(LED, HIGH); } // LED off
 Serial.println();
 Serial.print("fan_status = ");
 Serial.println(fan_status);
 Serial.println("-----------------------");
}
//  End of the Callback function to recieve and print the message that was sent to topic 'fan'
//********************************************************//
void loop() {
  //start of void loop
 client.loop();
 //***************************************************//
 // String   temperatureString = Serial2.readString();      // read and store the value of voltage sensor which recieved by UART2.
 //*************************************************//
 //Start the code to publish the battery temperature
 String temperatureString = "30.08"; // define the temperature reading as string, because the UART return string.
 char *temperature;  // define the temperature be published as char, because the UART return string.
 temperatureString.toCharArray(temperature, 30);
 client.publish("battery_temperature",temperature);
 delay(1000);
 client.publish("battery_temperature", "40.05");
 delay(1000);
 //Start the code to publish the battery temperature
 //*************************************************//
}
//End of void loop
