
from paho.mqtt import client as mqtt_client
import time
from datetime import date

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
global num_of_cycles
num_of_cycles = 0      # I have to read the number of dechasging cycles from a file.
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
            if num_of_cycles <= 100:
                soc_num_of_cycles_coeff = 1
            elif num_of_cycles > 100 and num_of_cycles <= 200:
                soc_num_of_cycles_coeff = 0.95
            return soc_num_of_cycles_coeff

        total_SOH = SOH_self_discharge() * SOH_num_of_cycles ()
        return total_SOH
    
    SOH  = int (100000*get_state_of_health ())
    #print (SOH)
    client.publish(topic ="SOH_cell1", payload= str(SOH) , qos=1)        #client.publish(topic ="SOH_cell1", payload= str(SOH) , qos=1)
    print("Cell_1 SOH= ",SOH/1000,"% \n")
    #******* End of the code to calculate the effect of number of cycles on total sate of health of the battery*********#
    #********* Start of get_thermal_coefficient_fun *********************************#
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
    cell1_state_of_charge= 100*soc (cell1_current,cell1_voltage,temperature)
    #**************************************************************************#
    def true_SOC (soc):
        if soc <= 0:
            soc=0
            global num_of_cycles
            num_of_cycles += 1 
        elif soc >= 100:
            soc= 100
            global num_of_cycles
            num_of_cycles += 1
        else:
            soc=soc
        return soc
    true_cell1_state_of_charge = float("{:.2f}".format(true_SOC (cell1_state_of_charge)))                     #convert to float of to decimal point.
    client.publish(topic ="soc_cell1", payload= str(true_cell1_state_of_charge), qos=1)                             # publish(topic, payload=None, qos=0, retain=False)
    print("Cell_1 SOC= ",true_cell1_state_of_charge,"% \n")
    #time.sleep(2)
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
    get_measurements_compute(client)
   
if __name__ == '__main__':
    run()


"""
/*************** Errors refrence **********************/
error = 5  --------------->   this means the user should replace the battery eith a new one.
"""