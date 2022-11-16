
from paho.mqtt import client as mqtt_client
import time
from datetime import date
from math import exp
import threading
import array

#************************intializations***************************#
global  cell1_voltage
cell1_voltage = 0
global cell1_current
cell1_current = 0
global temperature   # °C
temperature = 25.0
global state_of_charge
state_of_charge = 0.0
is_int_soc_done= False
# global num_of_cycles
# file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/num_of_cycles.txt", "r")   # open the file 'num_of_cycles.txt' in raeding mode.
# num_of_cycles = int (file.read()) 
# global error_soc
# error_soc = 0
# global msg_recieved_flag
# msg_recieved_flag = False
#*****************************************************************#
broker = 'broker.emqx.io'
port = 1883
topic = 'battery_temperature'
# generate client ID with pub prefix randomly
client_id = 'python_cloud'
#username = 'emqx'
#password = 'public'

#******************************************************************#
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
#******************************************************************#
def get_measurements_compute(client):
 while True:
    def on_message(client, userdata,msg):

        # check if the message recieved on 'battery_temperature'  topic, publish {ON,OFF} on topic 'fan' after recieving the temperature reading
        if msg.topic==str('battery_temperature'):
            
            temperature= (float) (msg.payload.decode())/10
            print("Received " + str(temperature)+ " from " + msg.topic + " topic")
            #global msg_recieved_flag
            #msg_recieved_flag = True
        # elif msg_recieved_flag == False:
        #     #global error_soc
        #     time.sleep(30)
        #     error_soc = 4


            # """create a function to publish {ON,OFF} on topic 'fan' after recieving the battery temberature reading"""
            # if  temperature >= 40:       
            #     client.publish('fan',1)      # to turn the fan ON

            # else:
            #     client.publish('fan',0) # to turn the fan OFF
        
        #***************************************************************#


        elif msg.topic==str('cell1_voltage'):  # recive the message on topic cell1_voltage 
            global cell1_voltage
            voltage = (float) (msg.payload.decode())
            cell1_voltage = voltage/1000
            print("Received " + str(cell1_voltage)+ " from " + msg.topic + " topic")
            # global msg_recieved_flag
            # msg_recieved_flag = True

        #elif msg_recieved_flag == False:
        #     #global error_soc
        #     time.sleep(3)
        #     error_soc = 3

        #************************************************************#
        elif msg.topic==str('cell1_current'):  # recive the message on topic cell1_current 
            global cell1_current
            current = (float)(msg.payload.decode())
            cell1_current = current/1000
            print("Received " + str(cell1_current)+ " from " + msg.topic + " topic")
            #global msg_recieved_flag
            #msg_recieved_flag = True

        # elif msg_recieved_flag == False:
        #     #global error_soc
        #     time.sleep(30)
        #     error_soc = 2
            
        #*******************************************************************************#
        elif msg.topic==str('sensors_Error'):  # recive the message on topic cell1_current 
            error = (int)(msg.payload.decode())
            if error == 1:
                client.publish('messages',"1")  # 1 means the sensors are not connected.
        #***********************************************************************************#
        
    client.subscribe([('battery_temperature', 0), ('cell1_voltage', 0), ('cell1_current', 0), ('sensors_Error', 0)])
    client.on_message = on_message 
    # if msg_recieved_flag == False:
    #         global error_soc
    #         time.sleep(3)
    #         error_soc = 2
    #***************************************************************************#
    def get_state_of_health ():
        #******* Start of the code to calculate the effect of self-discharge on total sate of health of the battery*********#
        def SOH_self_discharge():
            today = date.today()
            month_from_year = today.year - 2022
            month_from_month = today.month - 8
            total_number_of_months = 12* month_from_year + month_from_month     # get the total number of months.
            if total_number_of_months <= 2:
                soc_self_discharge_coeff = 1
            elif total_number_of_months > 2 and total_number_of_months <= 6:
                soc_self_discharge_coeff = 0.95
            elif total_number_of_months > 6 and total_number_of_months <= 24:
                soc_self_discharge_coeff = 1 - (total_number_of_months/100)
            elif total_number_of_months > 24 and total_number_of_months <= 36:
                soc_self_discharge_coeff = 0.76 - 0.05 *(total_number_of_months - 24)
            elif total_number_of_months > 36 and total_number_of_months <= 96:
                soc_self_discharge_coeff = 0.7 - 0.025 *(total_number_of_months - 24)
            else:
                #client.publish(topic ="errors", payload= 5 , qos=1)
                soc_self_discharge_coeff = 0
            return soc_self_discharge_coeff
        #print (SOH_self_discharge())
    #******* End of the code to calculate the effect of self-discharge on total sate of health of the battery********#
    #******* Start of the code to calculate the effect of number of cycles on total sate of health of the battery*********#
        def SOH_num_of_cycles ():     # not complete
            global num_of_cycles
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/num_of_cycles.txt", "r")   # open the file 'num_of_cycles.txt' in raeding mode.
            num_of_cycles = int (file.read())
            file.close() 
            global soc_num_of_cycles_coeff
            if num_of_cycles <= 100:
                soc_num_of_cycles_coeff = 1
            elif num_of_cycles > 100 and num_of_cycles <= 200:
                soc_num_of_cycles_coeff = 0.95
            elif num_of_cycles > 200 and num_of_cycles <= 500:
                soc_num_of_cycles_coeff = 0.85
            else:
                soc_num_of_cycles_coeff = 0.85
            return soc_num_of_cycles_coeff

        total_SOH = SOH_self_discharge() * SOH_num_of_cycles ()
        return total_SOH
    
    SOH  = int (100000*get_state_of_health ())
    #print (SOH)
    client.publish(topic ="SOH_cell1", payload= str(SOH) , qos=1)        #client.publish(topic ="SOH_cell1", payload= str(SOH) , qos=1)
    print("Cell_1 SOH= ",SOH/1000,"% \n")
    #******* End of the code to calculate the effect of number of cycles on total sate of health of the battery*********#
    #********* Start of get_thermal_coefficient_function *********************************#
    def get_thermal_coefficient(temperature):
            if temperature <= 25:
                thermal_coefficient=1
            elif temperature > 25 and temperature <= 50 :
                thermal_coefficient=0.95
            elif temperature > 50 and temperature <= 80 :
                thermal_coefficient=0.75
            else :
               thermal_coefficient=0.55
            return thermal_coefficient
    #********* End of get_thermal_coefficient_fun *********************************#
    def get_soc_ocv (ocv):         # function to get the intial SOC of  from the relation between SOC and open circuit voltage (OCV).
            if ocv <= 6.4:
                socIntial=0
            elif ocv >6.4 and ocv <= 7.00 :
                socIntial= 0.05
            elif ocv > 7.00  and ocv <= 7.4 :
                socIntial= 0.1
            elif ocv > 7.4 and ocv <= 7.6 :
                socIntial= 0.15
            elif ocv > 7.6 and ocv <= 7.68 :
                socIntial= 0.2
            elif ocv > 7.68 and ocv <= 7.8 :
                socIntial= 0.25
            elif ocv > 7.8 and ocv <= 7.84 :
                socIntial= 0.25
            elif ocv > 7.84 and ocv <= 7.9 :
                socIntial= 0.3
            elif ocv > 7.9 and ocv <= 7.92 :
                socIntial= 0.35
            elif ocv > 7.92 and ocv <= 7.96 :
                socIntial= 0.4
            elif ocv > 7.96 and ocv <= 7.98 :
                socIntial= 0.45
            elif ocv > 7.98 and ocv <= 8.00 :
                socIntial= 0.5
            elif ocv > 8.00 and ocv <= 8.02 :
                socIntial= 0.55
            elif ocv > 8.02 and ocv <= 8.04 :
                socIntial= 0.6
            elif ocv > 8.04 and ocv <= 8.06 :
                socIntial= 0.65
            elif ocv > 8.06 and ocv <= 8.08 :
                socIntial= 0.7
            elif ocv > 8.08 and ocv <= 8.1 :
                socIntial= 0.75
            elif ocv > 8.1 and ocv <= 8.12 :
                socIntial= 0.8
            elif ocv > 8.12 and ocv <= 8.16 :
                socIntial= 0.85
            elif ocv > 8.16 and ocv <= 8.2 :
                socIntial= 0.9
            elif ocv > 8.2 and ocv <= 8.4 :
                socIntial= 0.95
            else:
                socIntial= 1.00
            return socIntial
    #******************************************************************#
    def soc(cell_current,cell_voltage,temperature):
            max_cell_capacity = 0.6 * get_state_of_health ()          # 600 mAh =0.6 Ah max cell capacity != the rated cell capacity, the rated cell capacity in this project = 600 mAh, if the battery is new, then the max cell capacity = rated cell capacity
            time_two_readings = 2           # time between two readings.
            current = cell_current
            global state_of_charge
            global is_int_soc_done
            if (is_int_soc_done == False) and (cell_voltage != 0.0):
                state_of_charge= get_soc_ocv (cell_voltage)           # get intial SOC from the open circuit voltage curve.
                is_int_soc_done = True
            thermal_coefficient = get_thermal_coefficient (temperature)
            state_of_charge = state_of_charge + (current* (time_two_readings/3600)*thermal_coefficient)/ max_cell_capacity   #/3600 to convert from second to hour.
            time.sleep (2)                     # to wait 5 seconds between readings.
            return state_of_charge
    global cell1_state_of_charge
    cell1_state_of_charge= 100*soc (cell1_current,cell1_voltage,temperature)
    #**************************************************************************#
    def true_SOC (soc):
        if soc <= 0:
            soc=0
            global num_of_cycles
            num_of_cycles += 1
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/num_of_cycles.txt", "w")
            file.truncate()      # delete the last value of number of cycles.
            file.write(str(num_of_cycles))
            file.close()
        elif soc >= 100:
            soc= 100
        else:
            soc=soc
        return soc
    true_cell1_state_of_charge = float("{:.2f}".format(true_SOC (cell1_state_of_charge)))                     #convert to float of to decimal point.
    client.publish(topic ="soc_cell1", payload= str(true_cell1_state_of_charge), qos=1)                             # publish(topic, payload=None, qos=0, retain=False)
    print("Cell_1 SOC= ",true_cell1_state_of_charge,"% \n")
#************************* Start of battery_age_estimation method*****************************************#
    """ This method is coded according to the published paper: Muenzel, V.; de Hoog, J.; Brazil, M.; Vishwanath, A.; Kalyanaraman,
    S. A multi-factor battery cycle life prediction methodology for optimal battery management. 
    """
    def battery_age_estimation ():
        #******************* Start of battery_age_temperature method***********************************#
        def battery_age_temperature():
            global temperature                   # the real temperature of the battery cell.
            clT_array = array.array('f', [])   # clT_array: is the array of cycle life of temperature, 'f': stands for float.
            for i in range (0,4):
                a = 0.0039
                b = 1.95
                c = 67.51
                d = 2070
                nominal_temperature = 25
                num_cycle_life_temp = (a*pow(temperature,3) - b*pow(temperature,2) + c*temperature + d)/(a*pow(nominal_temperature,3) - b*pow(nominal_temperature,2) + c*nominal_temperature + d)
                clT_array.append (num_cycle_life_temp)  # adding an num_cycle_life_temp to the array.
                time.sleep(1)                    # 21600     # wait for 6 hours to get another value of num_cycle_life_temp.
            avr_num_cycle_life_temp= (clT_array[0]+clT_array[1]+clT_array[2]+clT_array[3])/4
            return avr_num_cycle_life_temp
        #******************* End of battery_age_temperature method***********************************#
        #********************************************************************************************#
        def battery_age_chg_dischg_current():
            def get_chg_dischg_current():
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
                total_dischg_time = 1                    #it should to be zero, but substituted with 1 to avoid a software error, and more 1 second will not affect on our calculations. 
                global cell1_current
                while timer < 50:         # 86400
                    #global before_SOC
                    global cell1_state_of_charge
                    before_SOC = cell1_state_of_charge
                    if current_status_flag == False:
                        time.sleep(60)
                        if cell1_current < 0:
                            current_status_flag = True
                        increased_SOC = cell1_state_of_charge - before_SOC
                        #global total_incresed_SOC
                        total_incresed_SOC += increased_SOC
                        #global total_chg_time
                        total_chg_time +=  60                                        # in secondes
                    else:
                        time.sleep(60)
                        if cell1_current > 0:
                            current_status_flag = False
                        #stop_time = datetime.datetime.now()
                        decresed_SOC = before_SOC - cell1_state_of_charge
                        #global total_decresed_SOC
                        total_decresed_SOC += decresed_SOC
                        #global total_dischg_time
                        total_dischg_time += 60
                    timer += 60
                  
            get_chg_dischg_current()
            global disch_current
            disch_current = 0.025  #((total_decresed_SOC*3350)/(total_dischg_time/(3600)))/3350      # in coulomb
            global charging_current
            charging_current =  0.7  #((total_incresed_SOC*3350)/(total_chg_time/(3600)))/3350
                 
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
        def battery_age_SOC_DOD():
            q = 1471
            u = 0.3369
            v = -2.295
            s = 214.3
            t = 0.6111
            SOC_array = array.array('f', [])
            for i in range (0,8):                               # it repeats 8 times.
                global cell1_state_of_charge
                SOC_array.append(cell1_state_of_charge)         # append a new value of the cell1_state of charge every 3 hours.
                time.sleep(10)    #10800                       # wait for 3 hours
            
            dod =  60  #max(SOC_array) - min(SOC_array)                                  # depth of discharge.
            average_SOC =  50 #(SOC_array[0]+SOC_array[1]+SOC_array[2]+SOC_array[3])/4
            nominal_dod = 100
            nominal_average_SOC = 50
            real_cycle_life = q+((u/(2*v))*(s+100*u)-200*t)*dod + s*average_SOC + t* pow(dod,2) + u*dod*average_SOC + v* pow(average_SOC,2)
            nominal_cycle_life = q+((u/(2*v))*(s+100*u)-200*t)*nominal_dod + s*nominal_average_SOC + t* pow(nominal_dod,2) + u*nominal_dod*nominal_average_SOC + v* pow(nominal_average_SOC,2)
            num_cycle_life_SOC_DOD = real_cycle_life / nominal_cycle_life
            return num_cycle_life_SOC_DOD
        #******************* End of battery_age_SOC_DOD method*******************************#
        thread_1 = threading.Thread(target=battery_age_temperature)
        thread_1.start()
        thread_2 = threading.Thread(target=battery_age_chg_dischg_current())
        thread_2.start()
        thread_3 = threading.Thread(target=battery_age_SOC_DOD)
        thread_3.start()
        #battery_age_chg_dischg_current()
        nominal_cycle_life = 649                                        # from battery datasheet.
        global num_cycle_life_disch_current
        global num_cycle_life_charging_current
        equivelant_battery_num_cycle_life = int (nominal_cycle_life * battery_age_temperature() * num_cycle_life_disch_current * num_cycle_life_charging_current * battery_age_SOC_DOD())
        return equivelant_battery_num_cycle_life
    #************************* End of battery_age_estimation method*****************************************#
    
    print ("Battery age (Number of cycle life)= ",battery_age_estimation ())
    #******************************************************************************#
    # def SOC_publish (state_of_charge, error_soc):
    #     if error_soc == 2 or error_soc == 3 or error_soc == 4 :
    #         """ 1- error_soc = 2  ----> no recieved current sensor reading, communication  failure between the cloud and gateway (ESP32).
    #             2- error_soc = 3  ----> no recieved voltage sensor reading, communication failure between the cloud and gateway (ESP32).
    #             3- error_soc = 4  ----> no recieved temperature sensor reading, communication failure between the cloud and gateway (ESP32)."""     
    #         client.publish ("messages", 'error_soc')     # publish the error code on the messages topic.
    #         print("Communication failure!\n")
    #     else:
    #         cell1_state_of_charge= 100*soc (cell1_current,cell1_voltage,temperature)
    #         print("Cell_1 SOC= ","{0:.2f}".format(cell1_state_of_charge),"% \n")
    # SOC_publish (state_of_charge, error_soc)
#***********************************************************************************#
def run():
    client = connect_mqtt()
    client.loop_start()
    thread_4 = threading.Thread(target=get_measurements_compute(client))
    thread_4.start()
    #get_measurements_compute(client)
    
if __name__ == '__main__':
    run()


"""
/*************** Errors refrence **********************/
error = 5  --------------->   this means the user should replace the battery eith a new one.
"""