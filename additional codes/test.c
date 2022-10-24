
#include<stdio.h>
#include <stdlib.h>
#include <string.h>
# include <stdint.h>
 

uint16_t  voltage_sensor ()
{

	 uint16_t voltageToSend = 1560;

     return voltageToSend;
  }
 /****************************************************/
 void uart_transmit (uint16_t data_to_send)
 {

	char  txdata [10];
    sprintf(txdata, "%u", data_to_send);
	printf("data is: %s \n",txdata);
   }

int main() 
{
    //uint16_t voltage_to_send = voltage_sensor ();
	uart_transmit (voltage_sensor ());
}
