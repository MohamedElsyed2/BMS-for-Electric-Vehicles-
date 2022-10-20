#include <cstring>
#include <iostream>
#include <stdlib.h>
 
using namespace std;
 
 

int main()
{
     
     cout<<"Enter the sensor reading= "; 
     string string_sensor_reading;
     cin>>string_sensor_reading;
     //String   string_sensor_reading = Serial2.readString();        // read and store the value of  sensor which recieved by UART2.
     //int voltageInteger = voltageString.toInt();           // convert from string to integer.
     //float voltageFloat= (float)voltageInteger/100;    // convert from integer to float and devided by 100 to get the real sensor value.
     cout<<"string_sensor_reading= " << string_sensor_reading << endl;  
     //Serial.println(voltageFloat);

     //begin code for creating an ID for every sensor reading
     //String string_sensor_reading = "v148";  // assigning value to string 
     
    int string_sensor_reading_length = string_sensor_reading.length();
    
    char char_sensor_reading [string_sensor_reading_length + 1];  // declaring character array with the length of the string voltage.

    strcpy(char_sensor_reading, string_sensor_reading.c_str());  // copying the contents of the string to char array.
 
    if (char_sensor_reading[0] == 'a')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell1_int_voltage =  atoi ( char_sensor_reading);  // convert char array  to integer
        cout<<"cell1_int_voltage= " <<cell1_int_voltage <<endl;  // print the value to be published later.
    }
    else if (char_sensor_reading[0] == 'b')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell2_int_voltage =  atoi ( char_sensor_reading);  // convert char array  to integer
        cout<<"cell2_int_voltage= " <<cell2_int_voltage <<endl; 
    }
    else if (char_sensor_reading[0] == 'c')   //check the ID of the sensor reading, then convert it to the true value without the ID.
    {   
        char_sensor_reading[0]='0';
        int cell3_int_voltage =  atoi ( char_sensor_reading);  // convert char array to integer
        cout<<"cell3_int_voltage= " <<cell3_int_voltage <<endl; 
    }  
    /*else if (char_sensor_reading[0] == 'd')   //check the ID of the sensor reading, then convert it to the true value without the ID.
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
    }*/
 
    return 0;
}