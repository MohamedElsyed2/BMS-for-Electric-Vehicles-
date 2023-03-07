# include <stdio.h>
# include <stdint.h>
#include <stdbool.h>
# include <string.h>

uint8_t check_cool_sys(float cool_sys_current,int cool_sys_is_ON){

    int cool_sys_error;
    if (cool_sys_is_ON ==1)
    {
        if (cool_sys_current <= 300)
        {
            cool_sys_error = 1;
        }
        else
        {
            cool_sys_error= 0;
        }
    }
    else
    {
        cool_sys_error= 0;
    }
    
    return cool_sys_error;
}

int main() {

    float cool_sys_current= 200;
    int cool_sys_is_ON = 1;
    uint8_t cool_sys_error = check_cool_sys(cool_sys_current, cool_sys_is_ON);

    if (cool_sys_error != 0)
    {
    char  txdata [35];
    char ID = 'D';
 	sprintf(txdata, "%c%d%d%d \r\n", ID, 0, 0, cool_sys_error);
 	// HAL_UART_Transmit(&huart6,(uint8_t *) txdata, strlen(txdata), 10);
    printf("%s",txdata);
    }
    return 0;
}


/*
    cool_sys_error:
    000: coolind system is OK.
    001 : coolind system is defect. 
*/