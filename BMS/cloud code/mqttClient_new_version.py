
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

"""def subscibe_message(client: mqtt_client):
   
    def on_message(client, userdata,msg):
        # global  cell1_voltage
        # global cell1_current
        # global temperature   # °C

        # check if the message recieved on 'battery_temperature'  topic, publish {ON,OFF} on topic 'fan' after recieving the temperature reading
        if msg.topic==str('battery_temperature'): 
            global temperature
            temperature= (float) (msg.payload.decode())
            print("Received " + str(temperature)+ " from " + msg.topic + " topic")

            #create a function to publish {ON,OFF} on topic 'fan' after recieving the battery temberature reading
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

            # create a function to publish on topic 'SOC_of_cell1' after recieving the cell voltage reading
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
    #**************************************************************************#
    print (cell1_voltage)

#***************************************************************************#
def run():
    
    client = connect_mqtt()
    subscibe_message(client)
    client.loop_forever()
    #print (cell1_voltage)
    #client.loop_stop()
    #print(cell1_current)"""
    
if __name__ == '__main__':
    run()
