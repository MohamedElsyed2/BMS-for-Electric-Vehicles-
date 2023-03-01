
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import dbcdcd
import time
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="46045",
  database="CBBMS_DB"
)
mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)

#cred = credentials.Certificate("E:\Masterarbeit\BMS-for-Electric-Vehicles-\cloud code\serviceAccountKey.json")

# # Initialize the app with a service account, granting admin privileges
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://cloud-based-bms-95343-default-rtdb.europe-west1.firebasedatabase.app/'
# })
# ref = db.reference('/')
# while True:
    
    # # ref.set({
    # #     'voltage': '4'
    # # })
    # cell1_voltage = 3.9
    # ref.update({'voltage': cell1_voltage})

    # ref = db.reference('/path/to/data')
    # state_of_health = 0.95
    # cell_number= 1
    # time_str = time.ctime(time.time())
    # ref.child("state_of_health").update({"cell"+str(cell_number)+"_SOH": state_of_health})
    # ref.child("cell"+str(cell_number)+"_SOH").child(time_str).update({"value": state_of_health, "time":time_str})

    # state_of_health = ref.child("state_of_health").child("cell"+str(cell_number)+"_SOH").get()
    # # #print(state_of_health)
    # # time.sleep(1)
    # timer = ref.child("timer").get()
    # print(timer)
    # cell1_voltage = ref.child("temperature").child("Module1_temperature").get()
    # print(cell1_voltage)

#timestamp = time.ctime(time.time())
#timestamp = time.time()
# # Store multiple values with a timestamp in a nested data structure
# d= 5
# #ref.push(value=d)
# ref.child('cell1_voltage').push({
#                                 'timestamp': timestamp, 'value': d
#                                 }
                            
# ref.push({
# 'timestamp': timestamp,
# 'data': new_value
# })

# Retrieve data from a nested data structure
# nested_ref = ref.child('cell1_voltage').key('-NOtmJl2ONVLHJAeLh2m')
# nested_data = nested_ref.get()
# print(nested_data)

# data = {"value": 21}
# #-------------------------------------------------------------------------------
# # Create Data

# ref.push(data)
# ref.child("cell1_voltage").child(timestamp).set(data)
# voltage = ref.child("cell1_voltage").child(timestamp).child('value').get()
# print(voltage)

#ref.child("cell1_voltage").child(timestamp).update({"value": 2})
# timeInt = int(timestamp.timestamp())
# print(timeInt)


# timestamp_str = time.ctime(time.time())  # Get the current time as a string
# print("String representation:", timestamp_str)

# # Convert the string representation to a time tuple
# timestamp_tuple = time.strptime(timestamp_str)

# # Convert the time tuple to an integer timestamp
# timestamp_int = float(time.mktime(timestamp_tuple))

# print("Integer timestamp:", timestamp_int)
# global i
                # i =i+1
                # key ='value'+str(i)
                # print(key)
                # ref.child('Module1_temperature').push({
                #                             timestamp: {
                #                                 'temperature': temperature
                #                             }
                #                         })