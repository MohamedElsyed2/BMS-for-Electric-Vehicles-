
from paho.mqtt import client as mqtt_client
from datetime import date
import time
#*******************************#
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
import mysql.connector
print("Thread1!")
#******************************************************************#
def connect_mqtt() -> mqtt_client:
    
    broker = 'broker.emqx.io'
    port = 1883
    #topic = 'battery_temperature'
   
    client_id = 'python_cloud'     # generate client ID
    #username = 'emqx'
    #password = 'public'
    def on_connect(client, userdata, flags, rc):
        if rc == 0:               # rc:  the reason Code.
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
#******************************************************************#
# #********************* stup the databse************#
# cred = credentials.Certificate("E:\Masterarbeit\BMS-for-Electric-Vehicles-\cloud code\serviceAccountKey.json")

# # Initialize the app with a service account, granting admin privileges
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://cloud-based-bms-95343-default-rtdb.europe-west1.firebasedatabase.app/'
# })
# ref = db.reference('/')

#*********** setup the sql database ***********#
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="46045",
  database="CBBMS_DB"
)
mycursor = mydb.cursor()
print("connected to the database")
#***********************************************#
def get_measurements_compute(client):
    while True:
        def on_message(client, userdata,msg):
            print("get measurment from MQTT!")
            # check if the message recieved on 'battery_temperature'  topic, publish {ON,OFF} on topic 'fan' after recieving the temperature reading
            if msg.topic==str('battery_temperature'):
                temperature= (float) (msg.payload.decode())/10

                sql = "INSERT INTO modules_temperature (module_ID,temperature) VALUES (%s, %s)"
                values = (1, temperature)
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()  # Commit the transaction
                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/temperature.txt", "w")
                #     file.truncate()      
                #     file.write(str(temperature))
                # finally:
                #     file.close()
               
                # time_str = time.ctime(time.time())
                # ref.child("temperature").update({"Module1_temperature": temperature})
                # ref.child("Module1_temperature").child(time_str).update({"value": temperature, "time":time_str})
                print("Received " + str(temperature)+ " from " + msg.topic + " topic")
            #***************************************************************#
            elif msg.topic==str('cell1_voltage'):  # recive the message on topic cell1_voltage 
                # global cell1_voltage
                voltage = (float) (msg.payload.decode())
                cell1_voltage = voltage/1000

                sql = "INSERT INTO voltage_measurements (module_ID, cell_ID,voltage) VALUES (%s, %s, %s)"
                values = (1,1, cell1_voltage)
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit() 

                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_voltage.txt", "w")
                #     file.truncate()     
                #     file.write(str(cell1_voltage))
                # finally:
                #     file.close()
                # time_str = time.ctime(time.time())
                # ref.child("voltage").update({"cell1_voltage": cell1_voltage})
                # ref.child("cell1_voltage").child(time_str).update({"value": cell1_voltage, "time":time_str})
                
                print("Received " + str(cell1_voltage)+ " from " + msg.topic + " topic")
            #************************************************************#
            #***************************************************************#
            elif msg.topic==str('cell2_voltage'):  
                voltage = (float) (msg.payload.decode())
                cell2_voltage = voltage/1000

                sql = "INSERT INTO voltage_measurements (module_ID, cell_ID,voltage) VALUES (%s, %s, %s)"
                values = (1,2, cell2_voltage)
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()

                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell2_voltage.txt", "w")
                #     file.truncate()      
                #     file.write(str(cell2_voltage))
                # finally:
                #     file.close()
                print("Received " + str(cell2_voltage)+ " from " + msg.topic + " topic")
                # time_str = time.ctime(time.time())
                # ref.child("voltage").update({"cell2_voltage": cell2_voltage})
                # ref.child("cell2_voltage").child(time_str).update({"value": cell2_voltage, "time":time_str})
            #************************************************************#
            #***************************************************************#
            elif msg.topic==str('cell3_voltage'):  
                voltage = (float) (msg.payload.decode())
                cell3_voltage = voltage/1000

                sql = "INSERT INTO voltage_measurements (module_ID, cell_ID,voltage) VALUES (%s, %s, %s)"
                values = (1,3, cell3_voltage)
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()

                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell3_voltage.txt", "w")
                #     file.truncate()     
                #     file.write(str(cell3_voltage))
                # finally:
                #     file.close()
                print("Received " + str(cell3_voltage)+ " from " + msg.topic + " topic")
                # time_str = time.ctime(time.time())
                # ref.child("voltage").update({"cell3_voltage": cell3_voltage})
                # ref.child("cell3_voltage").child(time_str).update({"value": cell3_voltage, "time":time_str})
            #************************************************************#
            #***************************************************************#
            elif msg.topic==str('module1_voltage'):  
                voltage = (float) (msg.payload.decode())
                module1_voltage = voltage/1000

                sql = "INSERT INTO modules_voltage (module_ID, voltage) VALUES (%s, %s)"
                values = (1, module1_voltage)
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()

                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_voltage.txt", "w")
                #     file.truncate()     
                #     file.write(str(module1_voltage))
                # finally:
                #     file.close()
                print("Received " + str(module1_voltage)+ " from " + msg.topic + " topic")
                # time_str = time.ctime(time.time())
                # ref.child("voltage").update({"module1_voltage": module1_voltage})
                # ref.child("module1_voltage").child(time_str).update({"value": module1_voltage, "time":time_str})
            #************************************************************#
            elif msg.topic==str('cell1_current'):  # recive the message on topic cell1_current 
                #global cell1_current
                current = (float)(msg.payload.decode())
                cell1_current = current/1000

                sql = "INSERT INTO current_measurements (module_ID, cell_ID,current) VALUES (%s, %s, %s)"
                values =  (1,1, cell1_current)
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()
                
                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_current.txt", "w")
                #     file.truncate()       
                #     file.write(str(cell1_current))
                # finally:
                #     file.close()
                print("Received " + str(cell1_current)+ " from " + msg.topic + " topic")
                # time_str = time.ctime(time.time())
                # ref.child("current").update({"cell1_current": cell1_current})
                # ref.child("cell1_current").child(time_str).update({"value": cell1_current, "time":time_str})
            #******************************************************************************#
            elif msg.topic==str('cell2_current'): 
                current = (float)(msg.payload.decode())
                cell2_current = current/1000

                sql = "INSERT INTO current_measurements (module_ID, cell_ID,current) VALUES (%s, %s, %s)"
                values =  (1,2, cell2_current)
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()

                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell2_current.txt", "w")
                #     file.truncate()       
                #     file.write(str(cell2_current))
                # finally:
                #     file.close()
                print("Received " + str(cell2_current)+ " from " + msg.topic + " topic")
                # time_str = time.ctime(time.time())
                # ref.child("current").update({"cell2_current": cell2_current})
                # ref.child("cell2_current").child(time_str).update({"value": cell2_current, "time":time_str})
            #*******************************************************************************#
            #************************************************************#
            elif msg.topic==str('cell3_current'): 
                current = (float)(msg.payload.decode())
                cell3_current = current/1000

                sql = "INSERT INTO current_measurements (module_ID, cell_ID,current) VALUES (%s, %s, %s)"
                values =  (1,3, cell3_current)
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()

                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell3_current.txt", "w")
                #     file.truncate()       
                #     file.write(str(cell3_current))
                # finally:
                #     file.close()
                print("Received " + str(cell3_current)+ " from " + msg.topic + " topic")
                # time_str = time.ctime(time.time())
                # ref.child("current").update({"cell3_current": cell3_current})
                # ref.child("cell3_current").child(time_str).update({"value": cell3_current, "time":time_str})
            #*******************************************************************************#
            #************************************************************#
            elif msg.topic==str('module1_current'): 
                current = (float)(msg.payload.decode())
                module1_current = current/1000

                sql = "INSERT INTO modules_current (module_ID, current) VALUES (%s, %s)"
                values =  (1, module1_current)
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()

                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_current.txt", "w")
                #     file.truncate()       
                #     file.write(str(module1_current))
                # finally:
                #     file.close()
                print("Received " + str(module1_current)+ " from " + msg.topic + " topic")
                # time_str = time.ctime(time.time())
                # ref.child("current").update({"module1_current": module1_current})
                # ref.child("module1_current").child(time_str).update({"value": module1_current, "time":time_str})
            #*******************************************************************************#
            elif msg.topic==str('sensors_Error'):  # recive the message on topic cell1_current 
                error = (int)(msg.payload.decode())
                if error == 1:
                    client.publish('messages',"1")  # 1 means the sensors are not connected.
            #***********************************************************************************#
        client.subscribe([('battery_temperature', 1), ('cell1_voltage', 1), ('cell2_voltage', 1),('cell3_voltage', 1),('module1_voltage', 1), 
                          ('cell1_current', 1),('cell2_current', 1), ('cell3_current', 1),('module1_current', 1),('sensors_Error', 1)])
        client.on_message = on_message 
#***********************************************************************************#
def run():
    # while True:
    client = connect_mqtt()
    client.loop_start()
    get_measurements_compute(client)
    
run()


"""
/*************** Errors refrence **********************/
error = 5  --------------->   this means the user should replace the battery eith a new one.
 if error_soc == 2 or error_soc == 3 or error_soc == 4 :
1- error_soc = 2  ----> no recieved current sensor reading, communication  failure between the cloud and gateway (ESP32).
2- error_soc = 3  ----> no recieved voltage sensor reading, communication failure between the cloud and gateway (ESP32).
3- error_soc = 4  ----> no recieved temperature sensor reading, communication failure between the cloud and gateway (ESP32).
"""