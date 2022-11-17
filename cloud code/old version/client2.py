
import paho.mqtt.client as mqtt #import the client1
import time
global fan_status
fan_status = 0
#######################################################################
def cycle_life():
    ############
    def on_message(client, userdata, message):
        global fan_status
        fan_status= float (str(message.payload.decode("utf-8")))
        print("message received " + str(message.payload.decode("utf-8"))+ " on topic " + message.topic)
        #print("message topic=",message.topic)
        #print("message qos=",message.qos)
        #print("message retain flag=",message.retain)
    ########################################
    broker_address='broker.emqx.io'
    #broker_address="iot.eclipse.org"
    global client
    client = mqtt.Client("client_3") #create new instance
    client.on_message=on_message #attach function to callback
    print("connecting to broker")
    client.connect(broker_address) #connect to broker
    client.subscribe('fan')
    #client.loop_start()         # make the client always connected and running.
#compute ()

    while True:         
        client.loop_start() #start the loop
    #     time.sleep(1) # wait
    #     #client.loop_stop() #stop the loop
    #     #time.sleep(2) # wait
    #     #global fan_flag
    #     global fan_status
    #     fan_status += 1
    #     print(fan_status)
cycle_life()