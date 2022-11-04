# python 3.6

import random
import time
from paho.mqtt import client as mqtt_client
#***********************************************************#
global  cell1_voltage
cell1_voltage = 0
global cell1_current
cell1_current = 0
global temperature   # °C
temperature = 30
global state_of_charge
state_of_charge = 0.0
int_soc_flag= False

#******************************************************************************#
broker = 'broker.emqx.io'   # I use the EMQX free online broker
port = 1883
topic = "fan"    # this is the topic name, if you want to publish or subscribe to another one, please generate another name

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc): # The broker sends acknowledgement signal to the client to ckeck the connection (on_connect).
        if rc == 0:
            print("Connected to EMQX Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)  # connect to the broker
    return client

#**********************************************************************#
def get_measurements_compute(client):
  while True:
    def on_message(client, userdata,msg):

        # check if the message recieved on 'battery_temperature'  topic, publish {ON,OFF} on topic 'fan' after recieving the temperature reading
        if msg.topic==str('battery_temperature'): 
            global temperature
            temperature= (float) (msg.payload.decode())
            print("Received " + str(temperature)+ " from " + msg.topic + " topic")

            # """create a function to publish {ON,OFF} on topic 'fan' after recieving the battery temberature reading"""
            # if  temperature >= 40:       
            #     client.publish('fan',1)      # to turn the fan ON

            # else:
            #     client.publish('fan',0) # to turn the fan OFF
        #***************************************************************#

        if msg.topic==str('cell1_voltage'):  # recive the message on topic cell1_voltage 
            global cell1_voltage
            voltage = (float) (msg.payload.decode())
            cell1_voltage = voltage/1000
            print("Received " + str(cell1_voltage)+ " from " + msg.topic + " topic")

            # """create a function to publish on topic 'SOC_of_cell1' after recieving the cell voltage reading"""
            # if  cell1_voltage >= 1.3:
            #     client.publish('SOC_of_cell1',1)      # to turn the fan ON
            # else:
            #     client.publish('SOC_of_cell1',0) # to turn the fan OFF

        #************************************************************#
        if msg.topic==str('cell1_current'):  # recive the message on topic cell1_current 
            global cell1_current
            current = (float)(msg.payload.decode())
            cell1_current = current/1000
            print("Received " + str(cell1_current)+ " from " + msg.topic + " topic")
            
        #*******************************************************************************#
        if msg.topic==str('sensors_Error'):  # recive the message on topic cell1_current 
            error = (int)(msg.payload.decode())
            if error ==1:
                client.publish('messages',"1")  # 1 means the sensors are not connected.
        #***********************************************************************************#
    client.subscribe([('battery_temperature', 0), ('cell1_voltage', 0), ('cell1_current', 0), ('sensors_Error', 0)])
    client.on_message = on_message
    #***************************************************************************#

    # def soc (current,voltage):
    #     print(current * voltage)
    #     time.sleep(2)
    # soc(cell1_current,cell1_voltage)
    #***************************************************************#
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
            if ocv <= 0.5:
                socIntial=0
            elif ocv >0.5 and ocv <= 0.6 :
                socIntial= 0.05
            elif ocv >0.6 and ocv <= 0.75 :
                socIntial= 0.1
            elif ocv >= 2.0 and ocv <= 4.0 :
                socIntial= 0.2  
            return socIntial
    #******************************************************************#
    def soc(cell_current,cell_voltage,temperature):
            max_cell_capacity = 0.6         # 600 mAh=0.6 Ah max cell capacity != the rated cell capacity, the rated cell capacity in this project = 600 mAh, if the battery is new, then the max cell capacity = rated cell capacity
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
    cell1_state_of_charge= soc(cell1_current,cell1_voltage,temperature)
    print("Cell_1 SOC= ",100*cell1_state_of_charge,"% \n")
#************************************************************************#
def run():
    client = connect_mqtt()
    client.loop_start()
    # client.loop_stop()
    #client.loop_forever()
    get_measurements_compute(client)
    


if __name__ == '__main__':
    run()
