
import paho.mqtt.client as mqtt #import the client1
import time
############
def on_message(client, userdata, message):
    print("message received " + str(message.payload.decode("utf-8"))+ " on topic " + message.topic)
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)
########################################
broker_address='broker.emqx.io'
#broker_address="iot.eclipse.org"
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic",'fan')
client.subscribe('fan')
print("Publishing message to topic",'battery_temperature')
for temperature in [20,21,25,30,35,20]:
    client.publish('battery_temperature',temperature)
while True:         #make the client always Running
    time.sleep(30) # wait
client.loop_stop() #stop the loop