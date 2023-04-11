
from paho.mqtt import client 
from math import exp
import threading
import time
import array
import datetime
import mysql.connector
#*********** setup the sql database ***********#
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="46045",
  database="CBBMS_DB"
)
mycursor = mydb.cursor()
mutex = threading.Lock()
#***********************************************#
#************************* Start of battery_age_estimation method*****************************************#
""" This method is coded according to the published paper: Muenzel, V.; de Hoog, J.; Brazil, M.; Vishwanath, A.; Kalyanaraman,
S. A multi-factor battery cycle life prediction methodology for optimal battery management. 
"""

#******************* Start of battery_age_temperature method***********************************#
def battery_age_temperature():
    
    sql = "SELECT temperature FROM modules_temperature WHERE module_ID = 1 ORDER BY ID DESC LIMIT 1"
    mutex.acquire()
    mycursor.execute(sql)
    data = mycursor.fetchone()
    mutex.release()
    temperature = data[0]
    clT_array = array.array('f', [])   # clT_array: is the array of cycle life of temperature, 'f': stands for float.
    for i in range (0,4):
        a = 0.0039
        b = 1.95
        c = 67.51
        d = 2070
        nominal_temperature = 25
        num_cycle_life_temp = (a*pow(temperature,3) - b*pow(temperature,2) + c*temperature + d)/(a*pow(nominal_temperature,3) - b*pow(nominal_temperature,2) + c*nominal_temperature + d)
        clT_array.append (num_cycle_life_temp)  # adding an num_cycle_life_temp to the array.
        time.sleep(21600)    # 21600     # wait for 6 hours to get another value of num_cycle_life_temp.
    global avr_num_cycle_life_temp
    avr_num_cycle_life_temp= (clT_array[0]+clT_array[1]+clT_array[2]+clT_array[3])/4
    #return avr_num_cycle_life_temp
#******************* End of battery_age_temperature method***********************************#
#********************************************************************************************#
def battery_age_chg_dischg_current(cell_number):
    def get_chg_dischg_current(cell_number):
        timer = 0
        global current_status_flag
        current_status_flag = False
        global total_incresed_SOC
        total_incresed_SOC = 0
        global total_decresed_SOC
        total_decresed_SOC = 0
        global total_chg_time
        total_chg_time = 0
        global total_dischg_time
        total_dischg_time = 1    
        
        sql = "SELECT current FROM modules_current WHERE module_ID = 1 ORDER BY ID DESC LIMIT 1"
        mutex.acquire()
        mycursor.execute(sql)
        data = mycursor.fetchone()
        mutex.release()
        cell_current = data[0]      
        while timer < 86400:         # 86400 wait for 24 hours
            
            sql = "SELECT SOC FROM cells_state_of_charge WHERE module_ID = 1 AND cell_ID = "+ str(cell_number) + " ORDER BY ID DESC LIMIT 1"
            mutex.acquire()
            mycursor.execute(sql)
            data = mycursor.fetchone()
            mutex.release()
            before_SOC = data[0]
            if current_status_flag == False:
                time.sleep(60) #60
                if cell_current > 0:              # positive  current means discharge current
                    current_status_flag = True
               
                sql = "SELECT SOC FROM cells_state_of_charge WHERE module_ID = 1 AND cell_ID = "+ str(cell_number) + " ORDER BY ID DESC LIMIT 1"
                mutex.acquire()
                mycursor.execute(sql)              
                data = mycursor.fetchone()
                mutex.release()
                SOC_after_chg = data[0]
                increased_SOC = SOC_after_chg - before_SOC
                #global total_incresed_SOC
                total_incresed_SOC += increased_SOC
                #global total_chg_time
                total_chg_time +=  60                                        # in secondes
            else:
                time.sleep(60)          #60
                if cell_current < 0:             # negative current means charge current
                    current_status_flag = False
                #stop_time = datetime.datetime.now()
                # file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_state_of_charge.txt", "r")   # open the file 'temperature.txt' in raeding mode.
                # SOC_after_dischg = float (file.read())
                # file.close()
                sql = "SELECT SOC FROM cells_state_of_charge WHERE module_ID = 1 AND cell_ID = "+ str(cell_number) + " ORDER BY ID DESC LIMIT 1"
                mutex.acquire()
                mycursor.execute(sql)
                data = mycursor.fetchone()
                mutex.release()
                SOC_after_dischg = data[0]
                decresed_SOC = before_SOC - SOC_after_dischg
                #global total_decresed_SOC
                total_decresed_SOC += decresed_SOC
                #global total_dischg_time
                total_dischg_time += 60
            timer += 60
            
    get_chg_dischg_current(cell_number)
    global disch_current
    disch_current = ((total_decresed_SOC*3350)/(total_dischg_time/(3600)))/3350      # in coulomb
    global charging_current
    charging_current = ((total_incresed_SOC*3350)/(total_chg_time/(3600)))/3350
            
    #********************************************************************************************#
    #******************* Start of battery_age_disch_current method*******************************#
    def battery_age_disch_current():
        global disch_current
        nominal_disch_current = 1                       # from datasheet
        e = 4464
        f = -0.1382
        g = -1519
        h = -0.4305
        global num_cycle_life_disch_current
        num_cycle_life_disch_current = (e*exp(f*disch_current)+g*exp(h*disch_current))/(e*exp(f*nominal_disch_current)+g*exp(h*nominal_disch_current))
        #return num_cycle_life_disch_current
    battery_age_disch_current()
    #******************* End of battery_age_disch_current method*******************************#
    #******************* Start of battery_age_charging_current method*******************************#
    def battery_age_charging_current():
        global charging_current
        nominal_charging_current = 0.7
        m = 5963
        n = -0.6531
        o = 321.4
        p = 0.03168
        global num_cycle_life_charging_current
        num_cycle_life_charging_current = (m*exp(n*charging_current)+o*exp(p*charging_current))/(m*exp(n*nominal_charging_current)+o*exp(p*nominal_charging_current))
        #return num_cycle_life_charging_current
    battery_age_charging_current()
    #******************* End of battery_age_charging_current method*******************************#
#******************* Start of battery_age_SOC_DOD method*******************************#
def battery_age_SOC_DOD(cell_number):
    q = 1471
    u = 0.3369
    v = -2.295
    s = 214.3
    t = 0.6111
    SOC_array = array.array('f', [])
    for i in range (0,8):                  # it repeats 8 times.
        #global cell_state_of_charge
        # file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_state_of_charge.txt", "r")   # open the file 'temperature.txt' in raeding mode.
        # cell_SOC = float (file.read())
        # file.close()
        sql = "SELECT SOC FROM cells_state_of_charge WHERE module_ID = 1 AND cell_ID = "+ str(cell_number) + " ORDER BY ID DESC LIMIT 1"
        mutex.acquire()
        mycursor.execute(sql)
        data = mycursor.fetchone()
        mutex.release()
        cell_SOC = data[0]
        SOC_array.append(cell_SOC)         # append a new value of the cell_state of charge every 3 hours.
        time.sleep(10800)    #10800                       # wait for 3 hours
    
    dod =  max(SOC_array) - min(SOC_array)                                  # depth of discharge.
    average_SOC =  (SOC_array[0]+SOC_array[1]+SOC_array[2]+SOC_array[3])/4
    nominal_dod = 100
    nominal_average_SOC = 50
    real_cycle_life = q+((u/(2*v))*(s+100*u)-200*t)*dod + s*average_SOC + t* pow(dod,2) + u*dod*average_SOC + v* pow(average_SOC,2)
    nominal_cycle_life = q+((u/(2*v))*(s+100*u)-200*t)*nominal_dod + s*nominal_average_SOC + t* pow(nominal_dod,2) + u*nominal_dod*nominal_average_SOC + v* pow(nominal_average_SOC,2)
    global num_cycle_life_SOC_DOD
    num_cycle_life_SOC_DOD = real_cycle_life / nominal_cycle_life
    #return num_cycle_life_SOC_DOD
#******************* End of battery_age_SOC_DOD method*******************************#

def run(cell_number):
    while True:
        thread_1 = threading.Thread(target=battery_age_temperature)
        thread_2 = threading.Thread(target=battery_age_chg_dischg_current, args=(cell_number,))
        thread_3 = threading.Thread(target=battery_age_SOC_DOD, args=(cell_number,))
        #start = time.time()
        thread_1.start()           # starting thread 1
        time.sleep(5)
        thread_2.start()            # starting thread 2
        time.sleep(5)
        thread_3.start()            # starting thread 3
        time.sleep(5)
        
        thread_1.join()                 # wait until thread 1 is completely executed
        thread_2.join()                  # wait until thread 2 is completely executed
        thread_3.join()                  # wait until thread 3 is completely executed
        #end = time.time()
        # all threads completely executed

        nominal_cycle_life = 649                  # from battery datasheet.
        global avr_num_cycle_life_temp
        global num_cycle_life_disch_current
        global num_cycle_life_charging_current
        residual_num_cycles = int (nominal_cycle_life * avr_num_cycle_life_temp * num_cycle_life_disch_current * num_cycle_life_charging_current * num_cycle_life_SOC_DOD)
        # print ("Battery age (Number of cycle life)= ",residual_num_cycles)
        #***** store the measurement value in MySQL database*****#
        sql = "INSERT INTO cells_residual_num_cycles (module_ID,cell_ID, residual_num_cycles) VALUES (%s, %s, %s)"
        values = (1,cell_number, residual_num_cycles)
        mutex.acquire()
        mycursor.execute(sql , values) 
        mydb.commit()  # Commit the transaction
        mutex.release()
#run(2)

