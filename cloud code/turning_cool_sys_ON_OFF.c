# include <stdio.h>
# include <stdint.h>
#include <stdbool.h>
# include <string.h>

int cool_sys_current_status = 0;

void check_cool_sys(int cool_sys_last_status ,int cool_sys_current_status){

    if (cool_sys_current_status != cool_sys_last_status){
        if(cool_sys_current_status == 1){
            // HAL_GPIO_WritePin(cooling_sys_input_GPIO_Port, cooling_sys_input_Pin, GPIO_PIN_SET);
            printf("%d\n", cool_sys_current_status);
        }
        else {
            // HAL_GPIO_WritePin(cooling_sys_input_GPIO_Port, cooling_sys_input_Pin, GPIO_PIN_RESET);
            printf("%d\n", cool_sys_current_status);
        }
    }
}

int main() {


    // int cool_sys_is_ON = 0;
    int cool_sys_last_status = cool_sys_current_status;
    int cool_sys_current_status = cool_sys_is_ON;
    check_cool_sys(cool_sys_last_status , cool_sys_current_status);
    return 0;
}

