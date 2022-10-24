
from paho.mqtt import client as mqtt_client
import time

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

def subscibe_publish(client: mqtt_client):
   
    def on_message(client, userdata,msg):

        if msg.topic==str('battery_temperature'): # check if the message recieved on 'battery_temperature'  topic, publish {ON,OFF} on topic 'fan' after recieving the temperature reading
            global temperature
            temperature= float(msg.payload.decode())
            print("Received " + str(temperature)+ " from " + msg.topic + " topic")

            """create a function to publish {ON,OFF} on topic 'fan' after recieving the battery temberature reading"""
            if  temperature >= 40:       
                client.publish('fan',1)      # to turn the fan ON

            else:
                client.publish('fan',0) # to turn the fan OFF
        #***************************************************************#

        elif msg.topic==str('cell1_voltage'):  # callback to get the cell1 voltage 
            global cell1_voltage
            cell1_voltage = float(msg.payload.decode())
            print("Received " + str(cell1_voltage)+ " from " + msg.topic + " topic")

            """create a function to publish on topic 'SOC_of_cell1' after recieving the cell voltage reading"""
            if  cell1_voltage >= 1.3:
                client.publish('SOC_of_cell1',1)      # to turn the fan ON
            else:
                client.publish('SOC_of_cell1',0) # to turn the fan OFF

        #************************************************************#

    client.subscribe([('battery_temperature', 0), ('cell1_voltage', 0)])
    client.on_message = on_message  
    #**************************************************************************#
# def relay_control(client: mqtt_client):
#     #****************************************
#     def on_message(client, userdata, msg):
#         global cell_voltage
#         cell_voltage = float(msg.payload.decode())
#         print("Received " + str(cell_voltage)+ " from " + msg.topic + " topic")

#         #************************************************************#
#         #create a function to publish {ON,OFF} on topic fan after recieving the temperature reading
#         if  cell_voltage >= 25:
#             client.publish('relay',1)      # to turn the fan ON

#         else:
#             client.publish('relay',0) # to turn the fan OFF
#         #************************************************************#

#     client.subscribe('cellVoltage')
#     client.on_message = on_message
    #***************************************************************************#

def run():
    client = connect_mqtt()
    subscibe_publish(client)
    #relay_control(client)
    #print (cell1_voltage)
    client.loop_forever()
    
if __name__ == '__main__':
    run()
