 
import time
import numpy
import threading
#*************************************************************************************#
def get_state_of_health (cell_number):
    if cell_number < 4:
        try:
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_state_of_health.txt", "r")  
            state_of_health = float (file.read())
        finally:
            file.close()
    elif cell_number == 4:
        try:
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_state_of_health.txt", "r")  
            state_of_health = float (file.read())
        finally:
            file.close()
    return state_of_health
#*************************************************************************************#
def get_intial_soc_calibration (cell_number,temperature, current, voltage):         
    #***********************************************************************************#
    if cell_number < 4:
        if current < 0 :          # In case of charging stage: if the current srnsor reading is negative, then the current is charging current.
            """Charging stage: in this experiment, the battery is first charged with a constant rate of 0.6C to a threshold voltage of 3.6 V, 
            and then charged with a constant voltage of 3.6 V to its full capacity. It can be observed that with the constant 
            charging current, the battery voltage increases gradually and reaches the threshold after 3200 s. After that, the battery 
            charged by the constant-voltage mode and the charging current drops rapidly in the first step, and then slowly. When the 
            current declines to 0.1C, the charging stage closes."""
            if temperature >= -5 and temperature < 15:
                rated_capacity = 3080 
                if voltage >= 4.2 and current >= -1.65:
                    def get_time_from_charging_current (current):
                        charging_time = [94.5 , 98, 106, 114 , 126 , 148 , 175]    # X-axis values
                        charging_current = [ 1.65, 1.25, 0.795 , 0.445 , 0.3 , 0.13 , 0.065 ]    # Y-axis values
                        chg_time = numpy.interp(current,  charging_current[::-1], charging_time[::-1],)
                        return chg_time

                    charging_time = [94.5 , 104 , 116.5, 135 , 175]  
                    capacity_axis = [2560 , 2750, 2880 , 2980, 3080] 
                    residual_capacity = numpy.interp(get_time_from_charging_current (abs(current)), charging_time[::1], capacity_axis[::1])
                #*******************************************************************************#
                elif voltage >= 3.75 and voltage < 4.2:           # from the battery datasheet, according to Charge Characteristics for NCR18650B1S.
                    def get_time_from_charging_voltage (voltage):
                        charging_time = [0.00 , 3.0 , 7.0 ,30.0 , 60.0 , 84.5 , 94.5]    # X-axis values
                        charging_voltage = [3.75, 3.76 , 3.755, 3.84 , 3.97 , 4.118 ,4.20 ]    # Y-axis values
                        chg_time = numpy.interp(voltage,  charging_voltage[::1], charging_time[::1],)
                        return chg_time

                    charging_time = [0.00 , 94.5]  
                    capacity_axis = [0.0, 2560 ] 
                    residual_capacity = numpy.interp(get_time_from_charging_voltage (voltage), charging_time[::1], capacity_axis[::1])    
                elif voltage < 3.75:        
                    residual_capacity = 0
                socIntial =  residual_capacity  / rated_capacity
            #**************************************************************#
                
            elif temperature >= 15 and temperature < 45:
                rated_capacity = 3350
                if voltage >= 4.2 and current >= -1.65:
                    def get_time_from_charging_current (current):
                        charging_time = [107, 110 , 113 , 120, 125 ,134 , 150 , 184]    # X-axis values
                        charging_current = [ 1.65 , 1.3 , 1.00 , 0.6 , 0.46 , 0.35 , 0.2 , 0.065 ]    # Y-axis values
                        chg_time = numpy.interp(current,  charging_current[::-1], charging_time[::-1],)
                        return chg_time

                    charging_time = [107 , 113, 120, 133 , 150 , 184]  
                    capacity_axis = [2900 , 3025, 3120, 3220, 3315, 3350] 
                    residual_capacity = numpy.interp(get_time_from_charging_current (abs(current)), charging_time[::1], capacity_axis[::1])
                #*******************************************************************************#
                elif voltage >= 3.3 and voltage < 4.2:           # from the battery datasheet, according to Charge Characteristics for NCR18650B1S.
                    def get_time_from_charging_voltage (voltage):
                        charging_time = [0.00 , 4.2 , 16 , 34 , 60 ,82.5 , 107]    # X-axis values
                        charging_voltage = [3.3 , 3.525, 3.58 , 3.7 , 3.83, 4.0 , 4.2 ]    # Y-axis values
                        chg_time = numpy.interp(voltage,  charging_voltage[::1], charging_time[::1],)
                        return chg_time

                    charging_time = [0.00 , 107]  
                    capacity_axis = [0.0, 2900 ] 
                    residual_capacity = numpy.interp(get_time_from_charging_voltage (voltage), charging_time[::1], capacity_axis[::1])    
                #************************************************************#
                elif voltage < 3.3:        
                    residual_capacity = 0
                socIntial =  residual_capacity  / rated_capacity

        #***********************************************************************#
        elif current >= 0 and current < 0.05:      # In case of open circuit voltage (OCV) stage, 0.05 --->  to take in mind the current losses.
            
            SOC = [0.00,0.00,0.00,5.00,10.00,15.00,20.00,25.00,30.00,35.00,40.00,45.00,50.00,55.00,60.00,65.00,70.00,75.00,80.00,85.00,90.00,95.00,100.00]    # SOC axis values
            OCV = [2.4,2.5,2.6,2.8,2.99,3.15,3.21,3.28,3.29,3.3,3.31,3.32,3.35,3.37,3.39,3.4,3.45,3.5,3.55,3.56,3.6,3.61,3.62]   # corresponding OCV axis values
            socIntial = numpy.interp(voltage, OCV[::1], SOC[::1])
        #*************************************************************************#
        elif current >= 0.05:                # In case of dicharging stage.
            try:
                file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_state_of_charge.txt", "r")  
                socIntial = float (file.read())
            except:
                time.sleep(0.1)
                socIntial = float (file.read())
            finally:
                file.close()
    
    # #************************************************************************************#
    elif cell_number == 4:         
        #????????????????????  I have to change the voltage and current to be the voltage and current of the whole module. ????????
        if current < 0 :          # In case of charging stage: if the current srnsor reading is negative, then the current is charging current.
            rated_capacity = 10050         # the rated capacity of the whole module at 25?? C. = 3350* 3 .
            if voltage >= 4.2 and current >= -1.65:
                def get_time_from_charging_current (current):
                    charging_time = [107, 110 , 113 , 120, 125 ,134 , 150 , 184]    # X-axis values
                    charging_current = [ 1.65 , 1.3 , 1.00 , 0.6 , 0.46 , 0.35 , 0.2 , 0.065 ]    # Y-axis values
                    chg_time = numpy.interp(current,  charging_current[::-1], charging_time[::-1],)
                    return chg_time

                charging_time = [107 , 113, 120, 133 , 150 , 184]  
                capacity_axis = [2900 , 3025, 3120, 3220, 3315, 3350] 
                residual_capacity = numpy.interp(get_time_from_charging_current (abs(current)), charging_time[::1], capacity_axis[::1])
            #*******************************************************************************#
            elif voltage >= 3.3 and voltage < 4.2:           # from the battery datasheet, according to Charge Characteristics for NCR18650B1S.
                def get_time_from_charging_voltage (voltage):
                    charging_time = [0.00 , 4.2 , 16 , 34 , 60 ,82.5 , 107]    # X-axis values
                    charging_voltage = [3.3 , 3.525, 3.58 , 3.7 , 3.83, 4.0 , 4.2 ]    # Y-axis values
                    chg_time = numpy.interp(voltage,  charging_voltage[::1], charging_time[::1],)
                    return chg_time

                charging_time = [0.00 , 107]  
                capacity_axis = [0.0, 2900 ] 
                residual_capacity = numpy.interp(get_time_from_charging_voltage (voltage), charging_time[::1], capacity_axis[::1])    
            #************************************************************#
            elif voltage < 3.3:        
                residual_capacity = 0
            socIntial =  residual_capacity  / rated_capacity

        #***********************************************************************#
        elif current >= 0 and current < 0.05:      # In case of open circuit voltage (OCV) stage, 0.05 --->  to take in mind the current losses.
            
            SOC = [0.00,0.00,0.00,5.00,10.00,15.00,20.00,25.00,30.00,35.00,40.00,45.00,50.00,55.00,60.00,65.00,70.00,75.00,80.00,85.00,90.00,95.00,100.00]    # SOC axis values
            
            OCV = [2.4,2.5,2.6,2.8,2.99,3.15,3.21,3.28,3.29,3.3,3.31,3.32,3.35,3.37,3.39,3.4,3.45,3.5,3.55,3.56,3.6,3.61,3.62]   # corresponding OCV axis values
            socIntial = numpy.interp(voltage, OCV[::1], SOC[::1])
        #*******************************************#
        elif current >= 0.05:                # In case of dicharging stage.
            try:
                file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_state_of_charge.txt", "r")  
                socIntial = float (file.read())
            finally:
                file.close()

    #***********************************************************************#
    return socIntial
#******************************************************************#
def get_coulombic_efficiency(cell_number):             # coulombic_efficiency at temberature 25?? C.
    if cell_number < 4:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_coulombic_efficiency.txt", "r")  
        coulombic_efficiency = float (file.read())
        file.close()
    elif cell_number == 4:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_coulombic_efficiency.txt", "r")  
        coulombic_efficiency = float (file.read())
        file.close()
    return coulombic_efficiency

#*********************************************************************#
def SoC_method(cell_number):
    while True:
        print ("state of charge is running")
        time.sleep(2)
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/temperature.txt", "r")  
        temperature = float (file.read())
        file.close()
        if cell_number < 4:
            rated_capacity = 3.350                                         # rated capacity (at 25?? C)
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_current.txt", "r")  
            current = float (file.read())
            file.close()
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_voltage.txt", "r")  
            voltage = float (file.read())
            file.close()
        elif cell_number == 4:
            rated_capacity = 10.05                                          # rate capacity for the the whole module = 3* 3.350 Ah
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_current.txt", "r")  
            current = float (file.read())
            file.close()
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_voltage.txt", "r")  
            voltage = float (file.read())
            file.close()
        global recalibrated_rated_capacity
        recalibrated_rated_capacity =  rated_capacity * get_state_of_health(cell_number)  
        coulombic_efficiency= get_coulombic_efficiency(cell_number)
        time_two_readings = 2           # time between two readings (2 sec).

        global state_of_charge
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/timer.txt", "r")   # open the file 'timer.txt' in raeding mode.
        timmer_interrupt = numpy.uint32 (file.read())                                # convert the string to unsigned int32.
        file.close() 
        if timmer_interrupt % 5 == 0:             # calibrate the SOC every 5 minutes.
            state_of_charge= get_intial_soc_calibration (cell_number,temperature, current, voltage)           # get intial SOC from the open circuit voltage curve.
        else:
            if cell_number < 4:
                try:
                    file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_state_of_charge.txt", "r")  
                    state_of_charge = float (file.read())
                finally:
                    file.close()
            elif cell_number == 4:
                try:
                    file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_state_of_charge.txt", "r")  
                    state_of_charge = float (file.read())
                finally:
                    file.close()
        state_of_charge = state_of_charge - coulombic_efficiency*(current* (time_two_readings/3600))/ recalibrated_rated_capacity   #/3600 to convert from second to hour.
        #*********** Start get the true SoC***********************************#
        if state_of_charge <= 0:
            state_of_charge=0
        elif state_of_charge >= 100:
            state_of_charge= 1
        else:
            state_of_charge = state_of_charge
        #****************** start code of update SoC********************#
        if cell_number < 4:
            try:
                file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_state_of_charge.txt", "w")
                file.truncate()       
                file.write(str(state_of_charge))
            finally:
                file.close()
        elif cell_number == 4:
            try:
                file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_state_of_charge.txt", "w")
                file.truncate()      
                file.write(str(state_of_charge))
            finally:
                file.close()   
        time.sleep (2)                     # to wait 2 seconds between readings.
#####################################################################################
def run():
    t_1 = threading.Thread(target=SoC_method, args=(1,))   # calculate the state of charge  of cell1.
    t_2 = threading.Thread(target=SoC_method, args=(2,))   # calculate the state of charge  of cell2.
    t_3 = threading.Thread(target=SoC_method, args=(3,))   # calculate the state of charge  of cell3.
    t_4 = threading.Thread(target=SoC_method, args=(4,))   # calculate the state of charge  of module1.
    t_1.start()
    t_2.start()
    t_3.start()
    t_4.start()

#run()