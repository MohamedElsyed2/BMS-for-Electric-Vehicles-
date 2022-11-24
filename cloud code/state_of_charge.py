 
import time
import numpy

#********* Start of get_thermal_coefficient_function *********************************#
# def get_thermal_coefficient(temperature):
#     if temperature <= 25:
#         thermal_coefficient=1
#     elif temperature > 25 and temperature <= 50 :
#         thermal_coefficient=0.95
#     elif temperature > 50 and temperature <= 80 :
#         thermal_coefficient=0.75
#     else :
#         thermal_coefficient=0.55
#     return thermal_coefficient
#********* End of get_thermal_coefficient_fun *********************************#
# """ This method is coded according to the published paper: Zhong, Q.; Huang, B.; Ma, J.; Li, H. Experimental Study on
# Relationship between SOC and voltage of Lithium-Ion Batteries. Int. J.Smart Grid Clean Energy 2014, 3, 149-153.
# """
def get_intial_soc_calibration (cell_number,temperature, current, voltage):         
    #***********************************************************************************#
    if current < 0 :          # In case of charging stage: if the current srnsor reading is negative, then the current is charging current.
        """Charging stage: in this experiment, the battery is first charged with a constant rate of 0.6C to a threshold voltage of 3.6 V, 
        and then charged with a constant voltage of 3.6 V to its full capacity. It can be observed that with the constant 
        charging current, the battery voltage increases gradually and reaches the threshold after 3200 s. After that, the battery 
        charged by the constant-voltage mode and the charging current drops rapidly in the first step, and then slowly. When the 
        current declines to 0.1C, the charging stage closes."""
        if temperature >= -5 and temperature < 15:
            if voltage < 4.2:          
                if voltage <= 3.75:        
                    socIntial=0
                elif voltage > 3.43 and voltage <= 3.48 :
                    socIntial= 0.05
                elif voltage > 3.48  and voltage <= 3.53 :
                    socIntial= 0.1
                elif voltage > 3.53 and voltage <= 3.55 :
                    socIntial= 0.15
                elif voltage > 3.96:
                    socIntial= 0.2
                elif voltage > 3.58 and voltage <= 3.61 :
                    socIntial= 0.25
                elif voltage > 3.61 and voltage <= 3.62 :
                    socIntial= 0.25
                elif voltage > 3.62 and voltage <= 3.63 :
                    socIntial= 0.3
        elif temperature >= 15 and temperature < 45:
            # get the values from the datasheet.
        

    #***********************************************************************#
    elif current >= 0 and current < 0.5:      # In case of open circuit voltage stage, 0.5 --->  to take in mind the current losses.
        if voltage <= 3.43:                             
            socIntial=0
        elif voltage > 3.43 and voltage <= 3.48 :
            socIntial= 0.05
        elif voltage > 3.48  and voltage <= 3.53 :
            socIntial= 0.1
        elif voltage > 3.53 and voltage <= 3.55 :
            socIntial= 0.15
        elif voltage > 3.55 and voltage <= 3.58 :
            socIntial= 0.2
        elif voltage > 3.58 and voltage <= 3.61 :
            socIntial= 0.25
        elif voltage > 3.61 and voltage <= 3.62 :
            socIntial= 0.25
        elif voltage > 3.62 and voltage <= 3.63 :
            socIntial= 0.3
        elif voltage > 3.63 and voltage <= 7.92 :
            socIntial= 0.35
        elif voltage > 7.92 and voltage <= 7.96 :
            socIntial= 0.4
        elif voltage > 7.96 and voltage <= 7.98 :
            socIntial= 0.45
        elif voltage > 7.98 and voltage <= 8.00 :
            socIntial= 0.5
        elif voltage > 8.00 and voltage <= 8.02 :
            socIntial= 0.55
        elif voltage > 8.02 and voltage <= 8.04 :
            socIntial= 0.6
        elif voltage > 8.04 and voltage <= 8.06 :
            socIntial= 0.65
        elif voltage > 8.06 and voltage <= 8.08 :
            socIntial= 0.7
        elif voltage > 8.08 and voltage <= 8.1 :
            socIntial= 0.75
        elif voltage > 8.1 and voltage <= 8.12 :
            socIntial= 0.8
        elif voltage > 8.12 and voltage <= 8.16 :
            socIntial= 0.85
        elif voltage > 8.16 and voltage <= 8.2 :
            socIntial= 0.9
        elif voltage > 8.2 and voltage <= 8.4 :
            socIntial= 0.95
        else:
            socIntial= 1.00
    else:                # In case of dicharging case.
        if cell_number == 1:
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_state_of_charge.txt", "r")  
            socIntial = float (file.read())
            file.close()
        elif cell_number == 2:
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell2_state_of_charge.txt", "r")  
            socIntial = float (file.read())
            file.close()
        elif cell_number == 3:
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell3_state_of_charge.txt", "r")  
            socIntial = float (file.read())
            file.close()
        elif cell_number == 4:
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell4_state_of_charge.txt", "r")  
            socIntial = float (file.read())
            file.close()
        elif cell_number == 5:
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_state_of_charge.txt", "r")  
            socIntial = float (file.read())
            file.close()
    return socIntial
#******************************************************************#
def soc(cell_number,cell_current,cell_voltage,temperature):
    file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_state_of_health.txt", "r")   # open the file 'temperature.txt' in raeding mode.
    state_of_health = float (file.read())
    file.close()
    rated_capacity = 3.350                                         # rated capacity (at 25° C)
    coulombic_efficiency= ???????????????????????  # must to be calculated firstly.
    #max_cell_capacity =  rated_capacity* state_of_health          
    time_two_readings = 2           # time between two readings.
    current = cell_current
    global state_of_charge
    file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/timer.txt", "r")   # open the file 'timer.txt' in raeding mode.
    timmer_interrupt = numpy.uint32 (file.read())                                # convert the string to unsigned int32.
    file.close() 
    if timmer_interrupt % 5 == 0:             # calibrate the SOC every 5 minutes.
        state_of_charge= get_intial_soc_calibration (cell_number,temperature,cell_current, cell_voltage)           # get intial SOC from the open circuit voltage curve.
        #is_int_soc_calibration_done = False
    #thermal_coefficient = get_thermal_coefficient (temperature)
    state_of_charge = state_of_charge - coulombic_efficiency*(current* (time_two_readings/3600))/ rated_capacity   #/3600 to convert from second to hour.
    time.sleep (2)                     # to wait 5 seconds between readings.
    return state_of_charge
# global cell1_state_of_charge
# cell1_state_of_charge= 100*soc (cell1_current,cell1_voltage,temperature)
#**************************************************************************#
def true_SOC (soc):
    if soc <= 0:
        soc=0
    elif soc >= 100:
        soc= 100
    else:
        soc=soc
    return soc
#####################################################################################


def run():
    while True:

        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_current.txt", "r")  
        cell1_current = float (file.read())
        file.close()
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_voltage.txt", "r")  
        cell1_voltage = float (file.read())
        file.close()
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/temperature.txt", "r")  
        temperature = float (file.read())
        file.close()
        true_cell1_state_of_charge = float("{:.2f}".format(true_SOC (100*soc (1, cell1_current,cell1_voltage,temperature))))                     #convert to float of to decimal point.
        #client.publish(topic ="soc_cell1", payload= str(true_cell1_state_of_charge), qos=1)                            # publish(topic, payload=None, qos=0, retain=False)
        print("Cell_1 SOC= ",true_cell1_state_of_charge,"% \n")
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_state_of_charge.txt", "w")
        file.truncate()       # delete the last value of number of cycles.
        file.write(str(true_cell1_state_of_charge))
        file.close()

#run()

#******************************************************************************#