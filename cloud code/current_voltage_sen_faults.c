#include <stdio.h>
#include <stdbool.h> // Include the header file for bool type
#include <math.h>
# include <string.h>

/****************************************************************************************************/
int check_current_sensors_fault (float current_sensor1,float current_sensor2, float current_sensor3,float module1_current_sensor){
    int error_code;
    
    if (abs(current_sensor1-current_sensor2)<= 300 && abs(current_sensor2-current_sensor3)<= 300 && abs(current_sensor3-module1_current_sensor)<= 300)
    {
        error_code= 0;
    }
    else if (abs(current_sensor1-current_sensor2)>= 300 &&abs(current_sensor2-current_sensor3)<= 300 && abs(current_sensor3-module1_current_sensor)<= 300) 
    {
    error_code = 1;
    }
    else if (abs(current_sensor1-current_sensor2)>= 300 && abs(current_sensor1-current_sensor3)<= 300 && abs(current_sensor3-module1_current_sensor)<= 300) 
    {
    error_code = 2;
    }
    else if (abs(current_sensor1-current_sensor2)<= 300  && abs(current_sensor2-current_sensor3)>= 300 && abs(current_sensor2-module1_current_sensor)<= 300) 
    {
    error_code = 3;
    }
    else if (abs(current_sensor1-current_sensor2)<= 300 && abs(current_sensor1-current_sensor3)<= 300 && abs(current_sensor3-module1_current_sensor)>= 300) 
    {
    error_code = 4;
    }
    else if (abs(current_sensor1-current_sensor2)>= 300 && abs(current_sensor3-module1_current_sensor)>= 300) {
        if (abs(current_sensor1-current_sensor3)<= 300 && abs(current_sensor2-module1_current_sensor)>= 300)
        {
            error_code = 24;
        }
        else if (abs(current_sensor1-module1_current_sensor)<= 300 && abs(current_sensor2-current_sensor3)>= 300)
        {
            error_code = 23;
        }
        else if (abs(current_sensor2-current_sensor3)<= 300 && abs(current_sensor1-module1_current_sensor)>= 300)
        {
            error_code = 14;
        }
        else if (abs(current_sensor2-module1_current_sensor)<= 300 && (abs(current_sensor1-current_sensor3)>= 300) || abs(current_sensor3-module1_current_sensor)>= 300)
        {
            error_code = 13;
        }
        
        }
    else if (abs(current_sensor1-current_sensor2)<= 300 && abs(current_sensor3-module1_current_sensor)>= 300)
    {
        error_code = 34;
    }
    
    else if (abs(current_sensor1-current_sensor2)>= 300 && abs(current_sensor3-module1_current_sensor)<= 300)
        {
            error_code = 12;
        }
    else{
            error_code=1234;
        }
return error_code;
}
/**************************************************************************************************/
int check_voltage_sensors_fault (float voltage_sensor1,float voltage_sensor2,float voltage_sensor3,float module1_voltage_sensor){
    int error_code2;
    float diff_12 = abs(voltage_sensor1-voltage_sensor2);
    float diff_13 = abs(voltage_sensor1-voltage_sensor3);
    float diff_23 = abs(voltage_sensor2-voltage_sensor3);
    float cell_vol_max = 4300;
    float cell_vol_min = 2500;
    bool cell1_ok= voltage_sensor1 >= cell_vol_min && voltage_sensor1 <= cell_vol_max ;
    bool cell2_ok= voltage_sensor2 >= cell_vol_min && voltage_sensor2 <= cell_vol_max ;
    bool cell3_ok= voltage_sensor3 >= cell_vol_min && voltage_sensor3 <= cell_vol_max ;
    
    if (cell1_ok && cell2_ok && cell3_ok){
        if (diff_12 >= 500) 
            {
                if (diff_23 <= 500)
                {
                    error_code2 = 1;
                }
                else{
                    error_code2 = 2;
                }
            }
        else if (diff_23 >= 500) 
            {
                if (diff_13 <= 500)
                {
                    error_code2 = 2;
                }
                else{
                    error_code2 = 3;
                }
            }
        else if (diff_13 >= 500) 
            {
                if (diff_12 <= 500)
                {
                    error_code2 = 3;
                }
                else{
                    error_code2 = 1;
                }
            }
        
        else if (diff_12 >= 500  && diff_13 >= 500 && diff_23 >= 500)
            {
                error_code2= 123;
            }
        else if (abs(module1_voltage_sensor-(voltage_sensor1+ voltage_sensor2+ voltage_sensor3))<= 500) 
            {
            error_code2 = 0;
            }
        else
        {
            error_code2= 4;
        }
    }
    return error_code2;
}
int main() {
    // int error_code = check_current_sensors_fault (current_sensor1,current_sensor2,current_sensor3,module1_current_sensor);
    int error_code = check_current_sensors_fault (1500,1400,1300,200);
    if (error_code != 0)
    {
    char  txdata [35];
    char ID = 'D';
 	sprintf(txdata, "%c%d \r\n", ID ,error_code);
 	//HAL_UART_Transmit(&huart6,(uint8_t *) txdata, strlen(txdata), 10);
    printf("%s",txdata);
    }

    // int error_code2 = check_voltage_sensors_fault (voltage_sensor1,voltage_sensor2,voltage_sensor3,module1_voltage_sensor);
    int error_code2 = check_voltage_sensors_fault (4200,3600,3600, 13300);
    if (error_code2 != 0)
    {
    char  txdata [35];
    char ID = 'D';
 	sprintf(txdata, "%c%d%d \r\n", ID, 0, error_code2);
 	// HAL_UART_Transmit(&huart6,(uint8_t *) txdata, strlen(txdata), 10);
    printf("%s",txdata);
    }
    return 0;
}


/* error code:
            0: all of the current sensors are OK.
            1 : current sensor#1 is defect.
            2 : current sensor#2 is defect.
            3 : current sensor#3 is defect.
            4 : module  sensor#1 is defect.
            12 : current sensor 1 & 2 maybe defect.
            13 : current sensor 1 & 3 maybe defect.
            14 : current sensor 1 & 4 maybe defect.
            23 : current sensor 2 & 3 maybe defect.
            24 : current sensor 2 & 4 maybe defect.
            34 :current sensor 3 & 4 maybe defect.

            00: all of the voltage sensors are OK.
            01 : voltage sensor#1 is defect.
            02 : voltage sensor#2 is defect.
            03 : voltage sensor#3 is defect.
            04 : voltage  sensor#1 is defect.
            0123: the voltage sensor 1 &2 & 3 maybe defect.
          
*/





