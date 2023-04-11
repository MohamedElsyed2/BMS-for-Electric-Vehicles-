# include <stdio.h>
# include <stdint.h>
#include <stdbool.h>
# include <string.h>

int heat_sys_current_status = 1;

uint8_t check_heat_sys(int heat_sys_last_status ,int heat_sys_current_status){

    if (heat_sys_current_status != heat_sys_last_status){
        if(heat_sys_current_status == 1){
            // HAL_GPIO_WritePin(cooling_sys_input_GPIO_Port, heating_sys_input_Pin, GPIO_PIN_SET);
            printf("%d\n", heat_sys_current_status);
        }
        else {
            // HAL_GPIO_WritePin(cooling_sys_input_GPIO_Port, heating_sys_input_Pin, GPIO_PIN_RESET);
            printf("%d\n", heat_sys_current_status);
        }
    }
}

int main() {


    int heat_sys_status = 0;
    int heat_sys_last_status = heat_sys_current_status;
    int heat_sys_current_status = heat_sys_status;
    check_heat_sys(heat_sys_last_status , heat_sys_current_status);
    return 0;
}

