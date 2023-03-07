# include <stdio.h>
# include <stdint.h>
#include <stdbool.h>
# include <string.h>

uint8_t check_cells_fault (uint16_t voltage_sensor1, uint16_t voltage_sensor2, uint16_t voltage_sensor3, uint16_t module1_voltage_sensor){

    // int cell_error;
    // if (cool_sys_is_ON ==1)
    // {
    //     if (cool_sys_current <= 300)
    //     {
    //         cell_error = 1;
    //     }
    //     else
    //     {
    //         cell_error= 0;
    //     }
    // }
    // else
    // {
    //     cell_error= 0;
    // }
    
    // return cell_error;
}

int main() {

    
    uint8_t cell_error = check_cells_fault (voltage_sensor1, voltage_sensor2, voltage_sensor3, module1_voltage_sensor);

    if (cell_error != 0)
    {
    char  txdata [35];
    char ID = 'D';
 	sprintf(txdata, "%c%d%d%d%d%d \r\n", ID, 0, 0,0,0, cell_error);
 	// HAL_UART_Transmit(&huart6,(uint8_t *) txdata, strlen(txdata), 10);
    printf("%s",txdata);
    }
    return 0;
}


/*
    cell_error:
    000: cooling system is OK.
    001 : cooling system is defect. 
*/