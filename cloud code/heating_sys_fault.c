# include <stdio.h>
# include <stdint.h>
#include <stdbool.h>
# include <string.h>

uint8_t check_heating_sys(float heat_sys_current,int heat_sys_status){

    int heat_sys_error;
    if (heat_sys_status ==1)
    {
        if (heat_sys_current <= 300)
        {
            heat_sys_error = 1;
        }
        else
        {
            heat_sys_error= 0;
        }
    }
    else
    {
        heat_sys_error= 0;
    }
    
    return heat_sys_error;
}

int main() {

    float heat_sys_current= 200;
    int heat_sys_status = 1;
    uint8_t heat_sys_error = check_heating_sys (heat_sys_current, heat_sys_status);

    if (heat_sys_error != 0)
    {
    char  txdata [35];
    char ID = 'D';
 	sprintf(txdata, "%c%d%d%d%d \r\n", ID, 0, 0, 0, heat_sys_error);
 	// HAL_UART_Transmit(&huart6,(uint8_t *) txdata, strlen(txdata), 10);
    printf("%s",txdata);
    }
    return 0;
}


/*
    heat_sys_error:
    0000: Heating system is OK.
    0001 : Heating system is defect. 
*/