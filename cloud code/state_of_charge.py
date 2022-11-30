 
import time
import numpy
#*************************************************************************************#
def get_state_of_health (cell_number):
    if cell_number == 1:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_state_of_health.txt", "r")  
        state_of_health = float (file.read())
        file.close()
    elif cell_number == 2:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell2_state_of_health.txt", "r")  
        state_of_health = float (file.read())
        file.close()
    elif cell_number == 3:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell3_state_of_health.txt", "r")  
        state_of_health = float (file.read())
        file.close()
    elif cell_number == 4:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell4_state_of_health.txt", "r")  
        state_of_health = float (file.read())
        file.close()
    elif cell_number == 5:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_state_of_health.txt", "r")  
        state_of_health = float (file.read())
        file.close()
    return state_of_health
#*************************************************************************************#
def get_intial_soc_calibration (cell_number,temperature, current, voltage):         
    #***********************************************************************************#
    if cell_number < 5:
        if current < 0 :          # In case of charging stage: if the current srnsor reading is negative, then the current is charging current.
            """Charging stage: in this experiment, the battery is first charged with a constant rate of 0.6C to a threshold voltage of 3.6 V, 
            and then charged with a constant voltage of 3.6 V to its full capacity. It can be observed that with the constant 
            charging current, the battery voltage increases gradually and reaches the threshold after 3200 s. After that, the battery 
            charged by the constant-voltage mode and the charging current drops rapidly in the first step, and then slowly. When the 
            current declines to 0.1C, the charging stage closes."""
            rated_capacity = 3350
            if temperature >= -5 and temperature < 15:
                if voltage >= 4.2:
                    if current < -1.4 and current >= -1.65:
                        residual_capacity = 2550
                    elif current < -1.2 and current >= -1.4:
                        residual_capacity = 2610
                    elif current < -1.0 and current >= -1.2:
                        residual_capacity = 2650
                    elif current < -0.8 and current >= -1.0:
                        residual_capacity = 2700
                    elif current < -0.6 and current >= -0.8:
                        residual_capacity = 2760
                    elif current < -0.4 and current >= -0.6:
                        residual_capacity = 2800
                    elif current < -0.2 and current >= -0.4:
                        residual_capacity = 2880
                    elif current < -0.12 and current >= -0.2:
                        residual_capacity = 2950
                    elif current < -0.065 and current >= -0.12:
                        residual_capacity = 3000
                    elif current > -0.065:
                        residual_capacity = 3100
                elif voltage >= 3.96 and voltage < 4.2:
                    residual_capacity = 3845 *(voltage-3.545)      # from the battery datasheet, according to Charge Characteristics for NCR18650B1S.
                elif voltage > 3.78 and voltage < 3.96 :
                    residual_capacity = 7061 *(voltage-3.725)
                elif voltage > 3.77 and voltage <= 3.78 :
                    residual_capacity= 268 
                elif voltage > 3.76 and voltage <= 3.77 :
                    residual_capacity= 218          
                elif voltage > 3.75 and voltage <= 3.76 :
                    residual_capacity= 1678     
                elif voltage <= 3.75:        
                    residual_capacity=0
                
            elif temperature >= 15 and temperature < 45:
                if voltage >= 4.2:
                    if current < -1.4 and current >= -1.65:
                        residual_capacity = 2850
                    elif current < -1.2 and current >= -1.4:
                        residual_capacity = 2940
                    elif current < -1.0 and current >= -1.2:
                        residual_capacity = 2990
                    elif current < -0.8 and current >= -1.0:
                        residual_capacity = 3030
                    elif current < -0.6 and current >= -0.8:
                        residual_capacity = 3100
                    elif current < -0.4 and current >= -0.6:
                        residual_capacity = 3150
                    elif current < -0.2 and current >= -0.4:
                        residual_capacity = 3200
                    elif current < -0.12 and current >= -0.2:
                        residual_capacity = 3280
                    elif current < -0.065 and current >= -0.12:
                        residual_capacity = 3000
                    elif current > -0.065:
                        residual_capacity = 3350   
                elif voltage >= 3.84 and voltage < 4.2 :                     # from the battery datasheet, according to Charge Characteristics for NCR18650B1S.
                    residual_capacity = 3570 *(voltage-3.375)  
                elif voltage >= 3.54 and voltage < 3.84 :
                    residual_capacity = 5040 *(voltage-3.516)         
                elif voltage >= 3.3 and voltage < 3.54 :
                    residual_capacity = 450 *(voltage-3.3)    
                elif voltage < 3.3:        
                    residual_capacity=0
            socIntial= residual_capacity/ rated_capacity

        #***********************************************************************#
        elif current >= 0 and current < 0.05:      # In case of open circuit voltage (OCV) stage, 0.05 --->  to take in mind the current losses.
            
            SOC = [0.00,0.00,0.00,5.00,10.00,15.00,20.00,25.00,30.00,35.00,40.00,45.00,50.00,55.00,60.00,65.00,70.00,75.00,80.00,85.00,90.00,95.00,100.00]    # SOC axis values
            
            OCV = [2.4,2.5,2.6,2.8,2.99,3.15,3.21,3.28,3.29,3.3,3.31,3.32,3.35,3.37,3.39,3.4,3.45,3.5,3.55,3.56,3.6,3.61,3.62]   # corresponding OCV axis values
            socIntial = numpy.interp(voltage, OCV[::1], SOC[::1])
        #*************************************************************************#
        elif current >= 0.05:                # In case of dicharging stage.
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
    
    # #************************************************************************************#
    elif cell_number == 5:
        if current < 0 :          # In case of charging stage: if the current srnsor reading is negative, then the current is charging current.
            rated_capacity = 13400
            ????????????????????????????????????????  #from here I have to change the values with the right one.
            if temperature >= -5 and temperature < 15:
                if voltage >= 4.2:
                    if current < -1.4 and current >= -1.65:
                        residual_capacity = 2550
                    elif current < -1.2 and current >= -1.4:
                        residual_capacity = 2610
                    elif current < -1.0 and current >= -1.2:
                        residual_capacity = 2650
                    elif current < -0.8 and current >= -1.0:
                        residual_capacity = 2700
                    elif current < -0.6 and current >= -0.8:
                        residual_capacity = 2760
                    elif current < -0.4 and current >= -0.6:
                        residual_capacity = 2800
                    elif current < -0.2 and current >= -0.4:
                        residual_capacity = 2880
                    elif current < -0.12 and current >= -0.2:
                        residual_capacity = 2950
                    elif current < -0.065 and current >= -0.12:
                        residual_capacity = 3000
                    elif current > -0.065:
                        residual_capacity = 3100
                elif voltage >= 3.96 and voltage < 4.2:
                    residual_capacity = 3845 *(voltage-3.545)      # from the battery datasheet, according to Charge Characteristics for NCR18650B1S.
                elif voltage > 3.78 and voltage < 3.96 :
                    residual_capacity = 7061 *(voltage-3.725)
                elif voltage > 3.77 and voltage <= 3.78 :
                    socIntial= 0.08 
                elif voltage > 3.76 and voltage <= 3.77 :
                    socIntial= 0.065          
                elif voltage > 3.75 and voltage <= 3.76 :
                    socIntial= 0.05     
                elif voltage <= 3.75:        
                    socIntial=0
                
            elif temperature >= 15 and temperature < 45:
                if voltage >= 4.2:
                    if current < -1.4 and current >= -1.65:
                        residual_capacity = 2850
                    elif current < -1.2 and current >= -1.4:
                        residual_capacity = 2940
                    elif current < -1.0 and current >= -1.2:
                        residual_capacity = 2990
                    elif current < -0.8 and current >= -1.0:
                        residual_capacity = 3030
                    elif current < -0.6 and current >= -0.8:
                        residual_capacity = 3100
                    elif current < -0.4 and current >= -0.6:
                        residual_capacity = 3150
                    elif current < -0.2 and current >= -0.4:
                        residual_capacity = 3200
                    elif current < -0.12 and current >= -0.2:
                        residual_capacity = 3280
                    elif current < -0.065 and current >= -0.12:
                        residual_capacity = 3000
                    elif current > -0.065:
                        residual_capacity = 3350   
                elif voltage >= 3.84 and voltage < 4.2 :                     # from the battery datasheet, according to Charge Characteristics for NCR18650B1S.
                    residual_capacity = 3570 *(voltage-3.375)  
                elif voltage >= 3.54 and voltage < 3.84 :
                    residual_capacity = 5040 *(voltage-3.516)         
                elif voltage >= 3.3 and voltage < 3.54 :
                    residual_capacity = 450 *(voltage-3.3)    
                elif voltage < 3.3:        
                    residual_capacity=0
            socIntial= residual_capacity/ rated_capacity

        #***********************************************************************#
        elif current >= 0 and current < 0.05:      # In case of open circuit voltage (OCV) stage, 0.05 --->  to take in mind the current losses.
            
            SOC = [0.00,0.00,0.00,5.00,10.00,15.00,20.00,25.00,30.00,35.00,40.00,45.00,50.00,55.00,60.00,65.00,70.00,75.00,80.00,85.00,90.00,95.00,100.00]    # SOC axis values
            
            OCV = [2.4,2.5,2.6,2.8,2.99,3.15,3.21,3.28,3.29,3.3,3.31,3.32,3.35,3.37,3.39,3.4,3.45,3.5,3.55,3.56,3.6,3.61,3.62]   # corresponding OCV axis values
            socIntial = numpy.interp(voltage, OCV[::1], SOC[::1])
        #*******************************************#
        elif current >= 0.05:                # In case of dicharging stage.
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_state_of_charge.txt", "r")  
            socIntial = float (file.read())
            file.close()

    #***********************************************************************#
    return socIntial
#******************************************************************#
def get_coulombic_efficiency(cell_number):             # coulombic_efficiency at temberature 25° C.
    if cell_number == 1:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_coulombic_efficiency.txt", "r")  
        coulombic_efficiency = float (file.read())
        file.close()
    elif cell_number == 2:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell2_coulombic_efficiency.txt", "r")  
        coulombic_efficiency = float (file.read())
        file.close()
    elif cell_number == 3:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell3_coulombic_efficiency.txt", "r")  
        coulombic_efficiency = float (file.read())
        file.close()
    elif cell_number == 4:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell4_coulombic_efficiency.txt", "r")  
        coulombic_efficiency = float (file.read())
        file.close()
    elif cell_number == 5:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_coulombic_efficiency.txt", "r")  
        coulombic_efficiency = float (file.read())
        file.close()
    return coulombic_efficiency

#*********************************************************************#
def soc(cell_number,cell_current,cell_voltage,temperature):
    
    if cell_number > 5:
        rated_capacity = 3.350                                         # rated capacity (at 25° C)
    elif cell_number == 5:
        rated_capacity = 13.4                                          # rate capacity for the the whole module = 4 * 3.350 Ah
    global recalibrated_rated_capacity
    recalibrated_rated_capacity =  rated_capacity * get_state_of_health(cell_number)  
    coulombic_efficiency= get_coulombic_efficiency(cell_number)
    time_two_readings = 2           # time between two readings (2 sec).
    current = cell_current
    global state_of_charge
    file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/timer.txt", "r")   # open the file 'timer.txt' in raeding mode.
    timmer_interrupt = numpy.uint32 (file.read())                                # convert the string to unsigned int32.
    file.close() 
    if timmer_interrupt % 5 == 0:             # calibrate the SOC every 5 minutes.
        state_of_charge= get_intial_soc_calibration (cell_number,temperature,cell_current, cell_voltage)           # get intial SOC from the open circuit voltage curve.
    #thermal_coefficient = get_thermal_coefficient (temperature)
    state_of_charge = state_of_charge - coulombic_efficiency*(current* (time_two_readings/3600))/ recalibrated_rated_capacity   #/3600 to convert from second to hour.
    time.sleep (2)                     # to wait 2 seconds between readings.
    return state_of_charge
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

        #************************************** Statrt calculation of cell1_SOC***************************************#
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
        file.truncate()       
        file.write(str(true_cell1_state_of_charge))
        file.close()
        #*********************************************End calculation of cell1_SOC****************************************#
        #************************************** Statrt calculation of cell2_SOC****************************************#


        ????????????????????? first read the cell current and voltage
        true_cell2_state_of_charge = float("{:.2f}".format(true_SOC (100*soc (2, cell2_current,cell2_voltage,temperature))))
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell2_state_of_charge.txt", "w")
        file.truncate()      
        file.write(str(true_cell2_state_of_charge))
        file.close()   
        #************************************** End calculation of cell2_SOC****************************************#

#run()

#******************************************************************************#