
#include<stdio.h>
#include <stdlib.h>
#include <string.h>
# include <stdint.h>
 

int  current_sensor ()
 {

	 float current = - 0.5*10;
	 int current_to_send = (int) current;
	 //string current_to_send = to_string (current);


     return current_to_send;
  }
 /****************************************************/
void uart_transmit (int data_to_send)
 {

	char  txdata [35];
    sprintf(txdata, "%d", data_to_send);
	printf("data is: %s \n",txdata);
   }

int main() 
{
	int result= current_sensor ();
    printf("\n The string for the num is %d \n", result);
    uart_transmit (result);
    

    return 0;
}
