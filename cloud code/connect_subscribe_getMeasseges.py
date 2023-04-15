
from paho.mqtt import client as mqtt_client
from datetime import date
import time
import threading
#*******************************#
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
import mysql.connector
mutex = threading.Lock()

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
client = connect_mqtt()
client.loop_start()
#******************************************************************#
#*********** setup the sql database ***********#
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="46045",
  database="CBBMS_DB"
)
mycursor = mydb.cursor()
#***********************************************#

def get_measurements_store_publish(client):
    
    while True:
        def on_message(client, userdata,msg):
            # check if the message recieved on 'battery_temperature'  topic, publish {ON,OFF} on topic 'fan' after recieving the temperature reading
            if msg.topic==str('battery_temperature'):
                temperature= (float) (msg.payload.decode())/10
                print("Received " + str(temperature)+ " from " + msg.topic + " topic")
                
                sql = "INSERT INTO modules_temperature (module_ID,temperature) VALUES (%s, %s)"
                values = (1, temperature)
                mutex.acquire()
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()  # Commit the transaction
                mutex.release()
                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/temperature.txt", "w")
                #     file.truncate()      
                #     file.write(str(temperature))
                # finally:
                #     file.close()
               
                # time_str = time.ctime(time.time())
                # ref.child("temperature").update({"Module1_temperature": temperature})
                # ref.child("Module1_temperature").child(time_str).update({"value": temperature, "time":time_str})
                #print("Received " + str(temperature)+ " from " + msg.topic + " topic")
            #***************************************************************#
            elif msg.topic==str('cell1_voltage'):  # recive the message on topic cell1_voltage 
                #******** save the recieved message in the required variable*****#
                voltage = (float) (msg.payload.decode())
                cell1_voltage = voltage/1000
                #****************************************************************#
                sql = "INSERT INTO voltage_measurements (module_ID, cell_ID,voltage) VALUES (%s, %s, %s)" # MySQL command to save the recieved measurement in the database.
                values = (1,1, cell1_voltage) # the values to be stored in the database.
                mutex.acquire()  # obtaining the database's lock before interacting with it.
                mycursor.execute(sql , values) # excute the required statement.
                mydb.commit()   # committing the data.
                mutex.release()  # relasing the database's lock after soring the data.
                print("Received " + str(cell1_voltage)+ " from " + msg.topic + " topic") # print statement to track the code.

                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_voltage.txt", "w")
                #     file.truncate()     
                #     file.write(str(cell1_voltage))
                # finally:
                #     file.close()
                # time_str = time.ctime(time.time())
                # ref.child("voltage").update({"cell1_voltage": cell1_voltage})
                # ref.child("cell1_voltage").child(time_str).update({"value": cell1_voltage, "time":time_str})
                
                
            #************************************************************#
            #***************************************************************#
            elif msg.topic==str('cell2_voltage'):  
                voltage = (float) (msg.payload.decode())
                cell2_voltage = voltage/1000

                sql = "INSERT INTO voltage_measurements (module_ID, cell_ID,voltage) VALUES (%s, %s, %s)"
                values = (1,2, cell2_voltage)
                mutex.acquire()
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()
                mutex.release()

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
                mutex.acquire()
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()
                mutex.release()

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
                mutex.acquire()
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()
                mutex.release()

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
            # elif msg.topic==str('cell1_current'):  # recive the message on topic cell1_current 
            #     #global cell1_current
            #     current = (float)(msg.payload.decode())
            #     cell1_current = current/1000

            #     sql = "INSERT INTO current_measurements (module_ID, cell_ID,current) VALUES (%s, %s, %s)"
            #     values =  (1,1, cell1_current)
            #     mutex.acquire()
            #     mycursor.execute(sql , values) # store the measurement value in SQL database
            #     mydb.commit()
            #     mutex.release()
                
            #     # try:
            #     #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_current.txt", "w")
            #     #     file.truncate()       
            #     #     file.write(str(cell1_current))
            #     # finally:
            #     #     file.close()
            #     print("Received " + str(cell1_current)+ " from " + msg.topic + " topic")
            #     # time_str = time.ctime(time.time())
            #     # ref.child("current").update({"cell1_current": cell1_current})
                # ref.child("cell1_current").child(time_str).update({"value": cell1_current, "time":time_str})
            #******************************************************************************#
            # elif msg.topic==str('cell2_current'): 
            #     current = (float)(msg.payload.decode())
            #     cell2_current = current/1000

            #     sql = "INSERT INTO current_measurements (module_ID, cell_ID,current) VALUES (%s, %s, %s)"
            #     values =  (1,2, cell2_current)
            #     mutex.acquire()
            #     mycursor.execute(sql , values) # store the measurement value in SQL database
            #     mydb.commit()
            #     mutex.release()

            #     # try:
            #     #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell2_current.txt", "w")
            #     #     file.truncate()       
            #     #     file.write(str(cell2_current))
            #     # finally:
            #     #     file.close()
            #     print("Received " + str(cell2_current)+ " from " + msg.topic + " topic")
                # time_str = time.ctime(time.time())
                # ref.child("current").update({"cell2_current": cell2_current})
                # ref.child("cell2_current").child(time_str).update({"value": cell2_current, "time":time_str})
            #*******************************************************************************#
            #************************************************************#
            # elif msg.topic==str('cell3_current'): 
            #     current = (float)(msg.payload.decode())
            #     cell3_current = current/1000

            #     sql = "INSERT INTO current_measurements (module_ID, cell_ID,current) VALUES (%s, %s, %s)"
            #     values =  (1,3, cell3_current)
            #     mutex.acquire()
            #     mycursor.execute(sql , values) # store the measurement value in SQL database
            #     mydb.commit()
            #     mutex.release()

            #     # try:
            #     #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell3_current.txt", "w")
            #     #     file.truncate()       
            #     #     file.write(str(cell3_current))
            #     # finally:
            #     #     file.close()
            #     print("Received " + str(cell3_current)+ " from " + msg.topic + " topic")
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
                mutex.acquire()
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()
                mutex.release()

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
             #************************************************************#
            elif msg.topic==str('module2_current'): 
                current = (float)(msg.payload.decode())
                module2_current = current/1000

                sql = "INSERT INTO modules_current (module_ID, current) VALUES (%s, %s)"
                values =  (2, module2_current)
                mutex.acquire()
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()
                mutex.release()
                print("Received " + str(module2_current)+ " from " + msg.topic + " topic")
            #***************************************************#
             #************************************************************#
            elif msg.topic==str('module3_current'): 
                current = (float)(msg.payload.decode())
                module3_current = current/1000

                sql = "INSERT INTO modules_current (module_ID, current) VALUES (%s, %s)"
                values =  (3, module3_current)
                mutex.acquire()
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()
                mutex.release()
                print("Received " + str(module3_current)+ " from " + msg.topic + " topic")
            #***************************************************#
            elif msg.topic==str('error_codes'): 
                sql = "SELECT heat_sys_error FROM error_codes ORDER BY ID DESC LIMIT 1" # SELECT SQL statement is used to retrieve the value of cooling_sys_status column
                mutex.acquire() #The mutex object is used to synchronize access to the database, ensuring that only one thread can access the database at a time
                mycursor.execute(sql)
                data = mycursor.fetchone() # retrieves the query result.
                mutex.release() # The mutex lock is then released
                heat_sys_error = data[0] 

                sql = "SELECT cool_sys_error FROM error_codes ORDER BY ID DESC LIMIT 1" # SELECT SQL statement is used to retrieve the value of cooling_sys_status column
                mutex.acquire() #The mutex object is used to synchronize access to the database, ensuring that only one thread can access the database at a time
                mycursor.execute(sql)
                data = mycursor.fetchone() # retrieves the query result.
                mutex.release() # The mutex lock is then released
                cool_sys_error = data[0] 

                sql = "SELECT current_sensor_error FROM error_codes ORDER BY ID DESC LIMIT 1" # SELECT SQL statement is used to retrieve the value of cooling_sys_status column
                mutex.acquire() #The mutex object is used to synchronize access to the database, ensuring that only one thread can access the database at a time
                mycursor.execute(sql)
                data = mycursor.fetchone() # retrieves the query result.
                mutex.release() # The mutex lock is then released
                current_sensor_error = data[0] 

                sql = "SELECT voltage_sensor_error FROM error_codes ORDER BY ID DESC LIMIT 1" # SELECT SQL statement is used to retrieve the value of cooling_sys_status column
                mutex.acquire() #The mutex object is used to synchronize access to the database, ensuring that only one thread can access the database at a time
                mycursor.execute(sql)
                data = mycursor.fetchone() # retrieves the query result.
                mutex.release() # The mutex lock is then released
                voltage_sensor_error = data[0] 

                sql = "SELECT cell_error FROM error_codes ORDER BY ID DESC LIMIT 1" # SELECT SQL statement is used to retrieve the value of cooling_sys_status column
                mutex.acquire() #The mutex object is used to synchronize access to the database, ensuring that only one thread can access the database at a time
                mycursor.execute(sql)
                data = mycursor.fetchone() # retrieves the query result.
                mutex.release() # The mutex lock is then released
                cell_error = data[0] 

                error_code = (int)(msg.payload.decode())
                
                if error_code <=1:
                    current_sensor_error = error_code

                elif error_code >=2 and error_code <= 7:
                    voltage_sensor_error = error_code
                
                elif error_code >=8 and error_code <= 9:
                    heat_sys_error = error_code

                elif error_code >=10 and error_code <= 11:
                    cool_sys_error = error_code

                else:
                    cell_error= error_code


                sql = "insert into error_codes (heat_sys_error , cool_sys_error ,current_sensor_error , voltage_sensor_error , cell_error) VALUES (%s, %s, %s, %s, %s)"
                values =  (heat_sys_error, cool_sys_error, current_sensor_error, voltage_sensor_error, cell_error)
                mutex.acquire()
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()
                mutex.release()
                print("Received " + str(error_code)+ " from " + msg.topic + " topic")
            #*******************************************************************************#
        client.subscribe([('battery_temperature', 1), ('cell1_voltage', 1), ('cell2_voltage', 1),('cell3_voltage', 1),('module1_voltage', 1), 
                          ('module1_current', 1), ('module2_current', 1),('module3_current', 1),('sensors_Error', 1),('error_codes', 1)])
        client.on_message = on_message 
    #****************************************************************************#
        def publish(client):
            #***** read the cooling system status, and sending it to the microcontroller***#
            sql = "SELECT cooling_sys_status FROM thermal_manag_sys ORDER BY ID DESC LIMIT 1" # SELECT SQL statement is used to retrieve the value of cooling_sys_status column
            mutex.acquire() #The mutex object is used to synchronize access to the database, ensuring that only one thread can access the database at a time
            mycursor.execute(sql)
            data = mycursor.fetchone() # retrieves the query result
            mutex.release() # The mutex lock is then released
            value_cool_sys = data[0]  # value of the cooling_sys_status is then extracted from the data variable and stored in value_cool_sys.
            client.publish('cooling_sys', str(value_cool_sys)) # the value is published to a message broker
            time.sleep(30)
            #*************************************************************************#
            #***** read the cooling system status, and sending it to the microcontroller***#
            sql = "SELECT heating_sys_status FROM thermal_manag_sys ORDER BY ID DESC LIMIT 1"
            mutex.acquire()
            mycursor.execute(sql)
            data = mycursor.fetchone()
            mutex.release()
            heating_sys_status = data[0]
            client.publish('heating_sys', str(heating_sys_status))
            time.sleep(30) 
            #*************************************************************************#

        publish(client)
        #********************************************#
def run():
    
    get_measurements_store_publish(client)
    
run()


"""
/*************** Errors refrence **********************/
error = 5  --------------->   this means the user should replace the battery eith a new one.
 if error_soc == 2 or error_soc == 3 or error_soc == 4 :
1- error_soc = 2  ----> no recieved current sensor reading, communication  failure between the cloud and gateway (ESP32).
2- error_soc = 3  ----> no recieved voltage sensor reading, communication failure between the cloud and gateway (ESP32).
3- error_soc = 4  ----> no recieved temperature sensor reading, communication failure between the cloud and gateway (ESP32).
"""
