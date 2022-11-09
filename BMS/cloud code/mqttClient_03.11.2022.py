
from paho.mqtt import client as mqtt_client
import time
#************************intializations***************************#
global  cell1_voltage
cell1_voltage = 0
global cell1_current
cell1_current = 0
global temperature   # °C
temperature = 25.0
global state_of_charge
state_of_charge = 0.0
int_soc_flag= False
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
    #***************************************************************#
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
            max_cell_capacity = 0.6         # 600 mAh =0.6 Ah max cell capacity != the rated cell capacity, the rated cell capacity in this project = 600 mAh, if the battery is new, then the max cell capacity = rated cell capacity
            time_two_readings = 2           # time between 2 readings.
            current = cell_current
            global state_of_charge
            global int_soc_flag
            if (int_soc_flag == False) and (cell_voltage != 0.0):
                state_of_charge= get_soc_ocv (cell_voltage)           # get intial SOC from the open circuit voltage curve.
                int_soc_flag = True
            thermal_coefficient = get_thermal_coefficient (temperature)
            state_of_charge = state_of_charge + (current* (time_two_readings/3600)*thermal_coefficient)/ max_cell_capacity   #/3600 to convert from second to hour.
            time.sleep (2)                     # to wait 5 seconds between readings.
            return state_of_charge
    cell1_state_of_charge= 100*soc (cell1_current,cell1_voltage,temperature)
    #**************************************************************************#
    def true_SOC (soc):
        if soc <= 0:
            soc=0
        elif soc >= 100:
            soc= 100
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
