
import time
from paho.mqtt import client as mqtt_client
global temperature

################################################################
broker = 'broker.emqx.io'   # I use the EMQX free online broker
port = 1883
#topic = "fan"    # this is the topic name, if you want to publish or subscribe to another one, please generate another name

# generate client ID with pub prefix randomly
# client_id = f'python-mqtt-{random.randint(0, 1000)}'
client_id = 'Cloud'  # to name the cloud client
username = 'emqx'
password = 'public'

##################################################################
def connect_mqtt():
    def on_connect(client, userdata, flags, rc): # The broker sends acknowledgement signal to the client to ckeck the connection (on_connect)
        # rc (return code) function is checking the connection status such as:
        # 0: Connection successful
        # 1: Connection failed: incorrect protocol version
        # 2: Connection failed: invalid client identifier
        # 3: Connection failed: server unavailable
        # 4: Connection failed: bad username or password
        # 5: Connection failed: not authorised
        # 6-255: Currently unused.
 
        if rc == 0:
            client.connected_flag=True #set flag
            print("Connected to \'" + broker +"\'Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    mqtt_client.Client.connected_flag=False
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.loop_start()
    print("Connecting to broker: ",broker)
    client.connect(broker, port)  # connect to the broker
    while not client.connected_flag: #wait to give the client a little bit time to connct to the broker
        print("connecting........")
        time.sleep(4)    
    client.loop_stop()    #Stop loop 
    return client

    #########################################################
def on_message(client, topic, message):
    global temperature
    temperature= float (str(message.payload.decode("utf-8")))
    print("message received " + str(message.payload.decode("utf-8"))+ " on topic " + message.topic)
#temp = temperature
client.subscribe([('battery_temperature', 0), ('cell1_voltage', 0), ('cell1_current', 0), ('sensors_Error', 0)])
client.on_message = on_message 

# #########################################################

# def publish(client,topic, message_to_send):
#     time.sleep(1)
#     result = client.publish(topic, message_to_send)
#         # result: [0, 1]
#     status = result[0]   #get publish acknacknowledge
#     if status == 0:
#         print(f"Send `{message_to_send}` to topic `{topic}`")
#     else:
#         print(f"Failed to send message to topic {topic}")
# ##############################################################
# def fan_control(client):
#     """create a function to publish {ON,OFF} on topic fan after recieving 
#     the temperature reading"""
#     global fan_flag
#     global fan_flag_current_State
#     fan_flag= False
#     #global topic
   
#     client.subscribe('battery_temperature')


#     # temperature_sensor_reading= [20,21,25,30,35,20]
#     #for battery_temperature in temperature_sensor_reading:
#     fan_flag_current_state = fan_flag  # to grt the fan ststus (on,off)

#     if not fan_flag_current_state and temperature > 25:
#         """if the fan is on and the temperature still more than 25,
#          do nothing. but if the fan is off and the temperature more 
#          than 25, then turn the fan on"""
#         publish(client,topic='fan',message_to_send=1) # to turn the fan ON
#         fan_flag= True

#     fan_flag_current_state= fan_flag
#     print(fan_flag_current_state)
#     if fan_flag_current_state and temperature <=25:
#         """if the fan is off and the temperature still less than 25, do nothing. but if the fan is on and the temperature less 
#         than 25, then turn the fan off"""
#         publish(client, topic= 'fan', message_to_send=0) # to turn the fan OFF
#         fan_flag= False
#         ############################################################

def run():
    client = connect_mqtt()
    client.loop_start()
    #fan_control(client)
    

if __name__ == '__main__':
    run()
