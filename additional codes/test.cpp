#include <cstring>
#include<stdio.h>
#include <stdlib.h>
#include <string.h>
 
 

uint16_t  voltage_sensor ()
{

	 uint16_t voltageToSend = 1560;

     return voltageToSend;
  }
 /****************************************************/
 void uart_1 (uint16_t data_to_send)
 {

	 char  txdata [35] = (char) data_to_send; //??????????????????????????????????
	
   }

int main() 
{
    //uint16_t voltage_to_send = voltage_sensor ();
	uart_1 (voltage_sensor ());
}
