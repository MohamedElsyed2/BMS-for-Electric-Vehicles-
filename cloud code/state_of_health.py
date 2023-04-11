
from datetime import date
from math import exp
import threading
import time
import os
import mysql.connector
#*********** setup the sql database ***********#
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="46045",
  database="CBBMS_DB"
)
mycursor = mydb.cursor()
#***********************************************#
mutex = threading.Lock()

""" These methods are coded according to the methodology which is published in: Andrea, Davide. Battery management systems for 
large lithium-ion battery packs. Artech house, 2010, pp. 189-192. And Tan, C.M., Singh, P. and Chen, C., 2020. Accurate real time 
on-line estimation of state-of-health and remaining useful life of Li ion batteries. Applied Sciences, 10(21), p.7836. """

def cal_state_of_health (cell_number):
    #while True:
        if cell_number < 4:
            def  get_nominal_lifetime (cell_number):
                """ This method is coded according to the published paper: Muenzel, V.; de Hoog, J.; Brazil, M.; Vishwanath, A.; Kalyanaraman,
                S. A multi-factor battery cycle life prediction methodology for optimal battery management. 
                """
                #**********************************************************************************#
                a = 0.0039
                b = 1.95
                c = 67.51
                d = 2070
                temperature = 25                   # the battery temperature will be constant at 25° C using the thermal management unit.
                nominal_temperature = 25
                num_cycle_life_temp = (a*pow(temperature,3) - b*pow(temperature,2) + c*temperature + d)/(a*pow(nominal_temperature,3) - b*pow(nominal_temperature,2) + c*nominal_temperature + d)
                #*************************************************************************************#
                disch_current = 0                 # no discharging current, beacuse the battery is out of sevice
                nominal_disch_current = 1                       # from datasheet
                e = 4464
                f = -0.1382
                g = -1519
                h = -0.4305
                num_cycle_life_disch_current = (e*exp(f*disch_current)+g*exp(h*disch_current))/(e*exp(f*nominal_disch_current)+g*exp(h*nominal_disch_current))
                #**********************************************************#
                charging_current = 0        # no charging current, beacuse the battery is out of sevice
                nominal_charging_current = 0.7        # from datasheet
                m = 5963
                n = -0.6531
                o = 321.4
                p = 0.03168
                num_cycle_life_charging_current = (m*exp(n*charging_current)+o*exp(p*charging_current))/(m*exp(n*nominal_charging_current)+o*exp(p*nominal_charging_current))

                #********* Start of nominal nominal cycle life due to DOD and SOCavg*************#
                q = 1471
                u = 0.3369
                v = -2.295
                s = 214.3
                t = 0.6111
                dod = 0     # the battery will not charge or discharge.
                sql = "SELECT SOC FROM cells_state_of_charge WHERE module_ID = 1 AND cell_ID = "+ str(cell_number)+"ORDER BY ID DESC LIMIT 1"
                mutex.acquire()
                mycursor.execute(sql)
                mutex.release()
                data = mycursor.fetchone()
                average_SOC = data[0]
                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_state_of_charge.txt", "r")   # open the file 'temperature.txt' in raeding mode.
                #     average_SOC = float (file.read())
                # finally:
                #     file.close()

                nominal_dod = 100         # from datasheet
                nominal_average_SOC = 50    # from datasheet
                real_cycle_life = q+((u/(2*v))*(s+100*u)-200*t)*dod + s*average_SOC + t* pow(dod,2) + u*dod*average_SOC + v* pow(average_SOC,2)
                nominal_cycle_life = q+((u/(2*v))*(s+100*u)-200*t)*nominal_dod + s*nominal_average_SOC + t* pow(nominal_dod,2) + u*nominal_dod*nominal_average_SOC + v* pow(nominal_average_SOC,2)
                num_cycle_life_SOC_DOD = real_cycle_life / nominal_cycle_life
                #****************************************************************************************#

                nominal_cycle_life = 649                                        # (day) from battery datasheet.
                equivelant_battery_num_cycle_life = int (nominal_cycle_life * num_cycle_life_temp * num_cycle_life_disch_current * num_cycle_life_charging_current * num_cycle_life_SOC_DOD)
                return equivelant_battery_num_cycle_life

            #******* Start of the code to calculate SoH based on the passage of time *********#
            def SOH_passage_of_time (cell_number):
                today = date.today()            # get the date of today.
                month_from_year = today.year - 2022   #  duration useage of the battery in years, 2022 is the year of first use. 
                month_from_month = today.month - 10    # duration useage of the battery in months, 10 is the month of first use.
                battery_age_month = 12* month_from_year + month_from_month     # calculate the total number of months.
                battery_age_year = battery_age_month / 12
                nominal_lifetime = get_nominal_lifetime (cell_number)/365     # number of life cycles when battery is not being used / 365 (assume that the battery will be charged once every day)  
                SoH_age = 1 - (battery_age_year / nominal_lifetime) 
                return SoH_age
            #****************************************************************************#

            #******* Start of the code to calculate SoH based on number of cycles *********#
            def SOH_num_of_cycles (cell_number):
                # file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_num_of_cycles.txt", "r")  
                # num_of_cycles = float (file.read())
                # file.close()
                sql = "SELECT num_of_cycles FROM cells_num_of_cycles WHERE module_ID = 1 AND cell_ID = "+ str(cell_number)
                mutex.acquire()
                mycursor.execute(sql) # ORDER BY ID DESC LIMIT 1
                data = mycursor.fetchall()
                mutex.release()
                last_value = data [-1]
                num_of_cycles = float (last_value[0])
                nominal_capacity = 3.350   # Ah
                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_current.txt", "r")  
                #     cell_current = float (file.read())
                # finally:
                #     file.close()
                mutex.acquire()
                sql = "SELECT current FROM modules_current WHERE module_ID = 1"
                mycursor.execute(sql)
                data = mycursor.fetchall()
                mutex.release()
                last_value = data [-1]
                cell_current = float (last_value[0])
                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/temperature.txt", "r")  
                #     temperature = float (file.read())
                # finally:
                #     file.close()
                mutex.acquire()
                mycursor.execute("SELECT temperature FROM modules_temperature WHERE module_ID = 1") # ORDER BY ID DESC LIMIT 1
                data = mycursor.fetchall()
                mutex.release()
                last_value = data [-1]
                temperature = float (last_value[0])

                c_rate = abs(cell_current)/nominal_capacity   
                temp_coeff = (temperature - 40 )/15                   # (temperature (◦C) - 40 ◦C)/15 ◦C, @ temperature 25° C.
                c_rate_coeff = c_rate - 2
                k1 = 0        #  k1 accounts for the capacity losses that increase rapidly during the conditions of cycling at high temperature.
                k2 = 0.000287 - 0.000115 * temp_coeff - 0.000080 * c_rate_coeff - 0.000032 *temp_coeff* c_rate_coeff       # k2 is a factor to account for capacity losses under the normal conditions of cycling.
                k3 = 0.003557 + 0.002207 * temp_coeff + 0.002843 * c_rate_coeff + 0.001493 * temp_coeff * c_rate_coeff       # k3 accounts for the capacity loss due to C-rate.
                soh_num_of_cycles_coeff = 1- (0.5*k1*pow(num_of_cycles,2)+k2 * num_of_cycles) - (k3*c_rate /nominal_capacity)
                return soh_num_of_cycles_coeff 
            #*************************************************************************************#
           
            mutex.acquire()
            mycursor.execute("SELECT value FROM battery_usage WHERE module_ID = 1") 
            data = mycursor.fetchall()
            mutex.release()
            last_value = data [-1]
            battery_being_used = float (last_value[0])
            if battery_being_used == 1:
                is_battery_being_used = True
            else:
                is_battery_being_used = False

            if is_battery_being_used == True:
                state_of_health = SOH_num_of_cycles (cell_number)
            else:
                state_of_health = SOH_passage_of_time (cell_number)
            total_SOH  = float("{:.2f}".format(state_of_health))               #convert to float of to decimal point.
           
            sql = "INSERT INTO cells_state_of_health (module_ID,cell_ID, SOH) VALUES (%s, %s, %s)"
            values = (1,cell_number, total_SOH)
            mutex.acquire()
            mycursor.execute(sql , values) # store the measurement value in SQL database
            mydb.commit()  # Commit the transaction
            mutex.release()
        #********************************************************************#
        elif cell_number == 4:
            soh = 0
            for cell_number in range(1,4):     # get the state of health of every cell.
                
                sql = "SELECT SOH FROM cells_state_of_health WHERE module_ID = 1 AND cell_ID = "+ str(cell_number)
                mycursor.execute(sql) 
                data = mycursor.fetchall()
                last_value = data [-1]
                soh += float (last_value[0])
            module1_SoH = soh / 3
            
            sql = "INSERT INTO modules_state_of_health (module_ID, SOH) VALUES (%s, %s)"
            values = (1, module1_SoH)
            mutex.acquire()
            mycursor.execute(sql , values) # store the measurement value in SQL database
            mutex.release()
            mydb.commit()  # Commit the transaction
        time.sleep(60)   # wait 60 sec between 2 loops.
#************************************************************************************************#    
def run():
    print ("state of health is running")
    # t_1 = threading.Thread(target=cal_state_of_health, args=(1,))   # calculate the state of health  of cell1.
    # t_2 = threading.Thread(target=cal_state_of_health, args=(2,))   # calculate the state of health  of cell2.
    # t_3 = threading.Thread(target=cal_state_of_health, args=(3,))   # calculate the state of health  of cell3.
    # t_4 = threading.Thread(target=cal_state_of_health, args=(4,))   # calculate the state of health  of module1.
    # t_1.start()
    # t_2.start()
    # t_3.start()
    # t_4.start()
    #while True:
    for i in range(4):
        cal_state_of_health(i+1)

#run()
