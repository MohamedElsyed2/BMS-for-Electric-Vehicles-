# include <stdio.h>
# include <stdint.h>
#include <stdbool.h>
# include <string.h>

uint8_t check_cells_fault (uint16_t voltage_sensor1, uint16_t voltage_sensor2, uint16_t voltage_sensor3){


    uint8_t error_code;
    bool cell1_fault = voltage_sensor1>= 4300 || voltage_sensor1 <= 2500;
    bool cell2_fault = voltage_sensor2>= 4300 || voltage_sensor2 <= 2500;
    bool cell3_fault = voltage_sensor3>= 4300 || voltage_sensor3 <= 2500;
    


    if (cell1_fault && cell2_fault && cell3_fault){
        error_code = 123;
    }
    else if (cell1_fault && cell2_fault){
        error_code = 12;
    }
    else if (cell2_fault && cell3_fault){
        error_code = 23;
    }
    else if (cell1_fault && cell3_fault){
        error_code = 13;
    }
    else if (cell1_fault){
        error_code = 1;
    }
    else if (cell2_fault){
        error_code = 2;
    }
    else if (cell3_fault){
        error_code = 3;
    }
    else {
        error_code =0;
    }
    
    // if (cell1_fault == 0 && cell2_fault == 0 && cell3_fault == 0){
    //     error_code = 0;
    // }
return error_code;
}

int main() {

    uint16_t voltage_sensor1= 4200;
    uint16_t voltage_sensor2 = 4200;
    uint16_t voltage_sensor3 = 5000;

    uint8_t cell_error = check_cells_fault (voltage_sensor1, voltage_sensor2, voltage_sensor3);
    
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
    00000: all cells are connected and there is no defect.
    00001 : cell #1 is not connected, short circuited, over-charged or over-discharged.
    00002 : cell #2 is not connected, short circuited, over-charged or over-discharged.
    00003 : cell #3 is not connected, short circuited, over-charged or over-discharged.
    000012: cells #1 and #2 are not connected, short circuited, over-charged or over-discharged.
    000013: cells #1 and #3 are not connected, short circuited, over-charged or over-discharged.
    000023: cells #2 and #3 are not connected, short circuited, over-charged or over-discharged.
    
*/