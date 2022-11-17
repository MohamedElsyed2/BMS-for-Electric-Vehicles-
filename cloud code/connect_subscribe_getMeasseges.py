
from paho.mqtt import client as mqtt_client
from datetime import date

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
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/temperature.txt", "w")
            file.truncate()      # delete the last value of number of cycles.
            file.write(str(temperature))
            file.close()
            print("Received " + str(temperature)+ " from " + msg.topic + " topic")
            #global msg_recieved_flag
            #msg_recieved_flag = True
        # elif msg_recieved_flag == False:
        #     #global error_soc
        #     time.sleep(30)
        #     error_soc = 4
        
        #***************************************************************#

        elif msg.topic==str('cell1_voltage'):  # recive the message on topic cell1_voltage 
            global cell1_voltage
            voltage = (float) (msg.payload.decode())
            cell1_voltage = voltage/1000
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_voltage.txt", "w")
            file.truncate()      # delete the last value of number of cycles.
            file.write(str(cell1_voltage))
            file.close()
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
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_current.txt", "w")
            file.truncate()       # delete the last value of number of cycles.
            file.write(str(cell1_current))
            file.close()
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
    
    # 
       
    #     else:
    #         cell1_state_of_charge= 100*soc (cell1_current,cell1_voltage,temperature)
    #         print("Cell_1 SOC= ","{0:.2f}".format(cell1_state_of_charge),"% \n")
    # SOC_publish (state_of_charge, error_soc)
#***********************************************************************************#
def run():
    client = connect_mqtt()
    client.loop_start()
    # thread_4 = threading.Thread(target=get_measurements_compute(client))
    # thread_4.start()
    get_measurements_compute(client)
    
# if __name__ == '__main__':
#     run()


"""
/*************** Errors refrence **********************/
error = 5  --------------->   this means the user should replace the battery eith a new one.
 if error_soc == 2 or error_soc == 3 or error_soc == 4 :
1- error_soc = 2  ----> no recieved current sensor reading, communication  failure between the cloud and gateway (ESP32).
2- error_soc = 3  ----> no recieved voltage sensor reading, communication failure between the cloud and gateway (ESP32).
3- error_soc = 4  ----> no recieved temperature sensor reading, communication failure between the cloud and gateway (ESP32).
"""