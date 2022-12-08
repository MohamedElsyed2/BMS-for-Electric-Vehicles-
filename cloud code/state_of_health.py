
import time
from datetime import date
import numpy
from math import exp
""" These methods are coded according to the methodology which is published in: Andrea, Davide. Battery management systems for 
large lithium-ion battery packs. Artech house, 2010, pp. 189-192. And Tan, C.M., Singh, P. and Chen, C., 2020. Accurate real time 
on-line estimation of state-of-health and remaining useful life of Li ion batteries. Applied Sciences, 10(21), p.7836. """

def get_state_of_health (cell_number):
    def get_nominal_lifetime (cell_number):
        a = 0.0039
        b = 1.95
        c = 67.51
        d = 2070
        temperature = 25                   # the battery temperature will be constant at 25° C using the thermal management unit.
        nominal_temperature = 25
        num_cycle_life_temp = (a*pow(temperature,3) - b*pow(temperature,2) + c*temperature + d)/(a*pow(nominal_temperature,3) - b*pow(nominal_temperature,2) + c*nominal_temperature + d)

        disch_current = 0                 # no discharging current.
        nominal_disch_current = 1                       # from datasheet
        e = 4464
        f = -0.1382
        g = -1519
        h = -0.4305
        num_cycle_life_disch_current = (e*exp(f*disch_current)+g*exp(h*disch_current))/(e*exp(f*nominal_disch_current)+g*exp(h*nominal_disch_current))


        charging_current = 0          # no charging current.
        nominal_charging_current = 0.7
        m = 5963
        n = -0.6531
        o = 321.4
        p = 0.03168
        num_cycle_life_charging_current = (m*exp(n*charging_current)+o*exp(p*charging_current))/(m*exp(n*nominal_charging_current)+o*exp(p*nominal_charging_current))

        q = 1471
        u = 0.3369
        v = -2.295
        s = 214.3
        t = 0.6111
        dod = 0     # the battery will not charge or discharge.
        try:
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_state_of_charge.txt", "r")   # open the file 'temperature.txt' in raeding mode.
            average_SOC = float (file.read())
        finally:
            file.close()

        nominal_dod = 100
        nominal_average_SOC = 50
        real_cycle_life = q+((u/(2*v))*(s+100*u)-200*t)*dod + s*average_SOC + t* pow(dod,2) + u*dod*average_SOC + v* pow(average_SOC,2)
        nominal_cycle_life = q+((u/(2*v))*(s+100*u)-200*t)*nominal_dod + s*nominal_average_SOC + t* pow(nominal_dod,2) + u*nominal_dod*nominal_average_SOC + v* pow(nominal_average_SOC,2)
        num_cycle_life_SOC_DOD = real_cycle_life / nominal_cycle_life


        nominal_cycle_life = 649                                        # from battery datasheet.
        equivelant_battery_num_cycle_life = int (nominal_cycle_life * num_cycle_life_temp * num_cycle_life_disch_current * num_cycle_life_charging_current * num_cycle_life_SOC_DOD)
        return equivelant_battery_num_cycle_life
    #******* Start of the code to calculate SoH based on the passage of time *********#
    def SOH_passage_of_time (cell_number):
        today = date.today()
        month_from_year = today.year - 2022
        month_from_month = today.month - 8
        battery_age_month = 12* month_from_year + month_from_month     # get the total number of months.
        battery_age_year = battery_age_month / 12
        nominal_lifetime = get_nominal_lifetime (cell_number)/365      # number of life cycles when battery is not being used / 365 (assume that the battery will be charged once every day)  
        soc_self_discharge_coeff = 1 - (battery_age_year / nominal_lifetime) 
        return soc_self_discharge_coeff
    #******* End of the code to calculate SoH based on the passage of time********#
    #******* Start of the code to calculate SoH based on number of cycles *********#
    def SOH_num_of_cycles (cell_number):
        if cell_number < 4:
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_num_of_cycles.txt", "r")  
            num_of_cycles = float (file.read())
            file.close()
            nominal_capacity = 3.350   # Ah
            # cycle_number_axis = [0, 500]    # y-axis values.
            # capacity_axis = [3350 , 2875]   # corresponding  x-axis values
            # current_rated_capacity = numpy.interp(num_of_cycles,cycle_number_axis[::1], capacity_axis[::1])
            # soh_num_of_cycles_coeff = current_rated_capacity / nominal_capacity
            k1 = ???????????????????????????    #  k1 accounts for the capacity losses that increase rapidly during the conditions of cycling at high temperature.
            k2 =   ???????????????              # k2 is a factor to account for capacity losses under the normal conditions of cycling.
            k3 = ???????????????                # k3 accounts for the capacity loss due to C-rate.
            try:
                file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_current.txt", "r")  
                cell_current = float (file.read())
            finally:
                file.close()
            c_rate = abs(cell_current)/nominal_capacity   ?????????????
            soh_num_of_cycles_coeff = 1- (0.5*k1*pow(num_of_cycles,2)+k2 * num_of_cycles) - (k3*c_rate /nominal_capacity)
           
        elif cell_number == 4:
            soh = 0
            for cell_number in range(1,4):     # get the state of health of every cell.
                file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_state_of_health.txt", "r")  
                soh += float (file.read())
                file.close()
            soh_num_of_cycles_coeff = soh / 3
        return soh_num_of_cycles_coeff 
    #******* End of the code to calculate SoH based on number of cycles*********#
    try:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/check_battery_being_used.txt", "r")   # open the file 'temperature.txt' in raeding mode.
        battery_being_used = int (file.read())
    finally:
        file.close()
    if battery_being_used == 1:
        is_battery_being_used = True
    else:
        is_battery_being_used = False

    if is_battery_being_used == True:
        state_of_health = SOH_num_of_cycles (cell_number)
    else:
        state_of_health = SOH_passage_of_time (cell_number)
    return state_of_health
    
def run():
    while True:
        for cell_number in range(1,4):     # calculate the state of health  of cell1, cell2, and  cell3.
            total_SOH  = float("{:.2f}".format(get_state_of_health (cell_number)))               #convert to float of to decimal point.
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_state_of_health.txt", "w")
            file.truncate()       
            file.write(str(total_SOH))
            file.close()
       #************************************** Statrt calculation of module1_SOC****************************************#
        module1_SOH= float("{:.2f}".format(get_state_of_health (4)))
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_state_of_health.txt", "w")
        file.truncate()      
        file.write(str(module1_SOH))
        file.close()   
        #************************************** End calculation of Module1_SOC****************************************#

#run()
