import threading
import mysql.connector

#*********** setup the sql database ***********#
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="46045",
  database="CBBMS_DB"
)
mycursor = mydb.cursor()
#***********************************************#
mutex = threading.Lock()
#**** insert a new value*******#

#mycursor.execute("INSERT INTO cell_data (voltage) VALUES (%s)",cell1_voltage)
#mydb.commit()
#values = (cell1_voltage)

# cell1_voltage = 3.5
# cell1_current = 1.8
# value = (1,3, cell1_voltage)
# Execute the SQL statement with the value as a parameter
# mycursor.execute("INSERT INTO voltage_measurements (module_ID, cell_ID,voltage) VALUES (%s, %s, %s)", value) # store the measurement value in SQL database
# mydb.commit()  # Commit the transaction
#mycursor.execute("CREATE TABLE current_measurement (module_ID int, cell_ID int, current float)")
# temperature = 25
# state_of_charge = 0.98
# sql = "INSERT INTO modules_temperature (module_ID,temperature) VALUES (%s, %s)"
# values = (1, temperature)
# mycursor.execute(sql , values) # store the measurement value in SQL database
# mydb.commit()  # Commit the transaction
#cell_number = 1
# sql = "SELECT SOC FROM cells_state_of_charge WHERE module_ID = 1 AND cell_ID = "+ str(cell_number)
# mycursor.execute(sql) 
# data = mycursor.fetchall()
# last_value = data [-1]
# socIntial = float (last_value[0])
# sql = "SELECT timer_value FROM timer ORDER BY ID DESC LIMIT 1"
# mycursor.execute(sql)
# data = mycursor.fetchone()
# timer_1 = data[0]
# calibrated_coulombic_Efficiency = 1
# sql = "INSERT INTO cells_coulombic_efficiency (module_ID,cell_ID, coulombic_efficiency) VALUES (%s, %s, %s)"
# values = (1,cell_number, calibrated_coulombic_Efficiency)
# mycursor.execute(sql , values) # store the measurement value in SQL database
# mydb.commit()  # Commit the transaction
#mycursor.execute("INSERT INTO modules_temperature (module_ID,temperature) VALUES (%s, %s)",(1, 20.5)) # store the measurement value in SQL database
# #********************************#
# mycursor.execute("SELECT temperature FROM modules_temperature") # ORDER BY ID DESC LIMIT 1
# temperature = mycursor.fetchall()
# last_value = temperature[-1]
# print(temperature)
sql = "SELECT heating_sys_status FROM thermal_manag_sys ORDER BY ID DESC LIMIT 1"
mycursor.execute(sql)
data = mycursor.fetchone()
value_cool_sys = data[0]
print(value_cool_sys)
#***** read the last value in a specific column*****#
#mycursor.execute("SELECT voltage FROM voltage_measurements WHERE cell_ID = 2") # ORDER BY ID DESC LIMIT 1
# cell3_values = mycursor.fetchall()
# #last_value = cell3_values[-1]
# print(cell3_values)
#print(last_value)
# print(float(last_value[0]))

# mycursor.execute("SELECT current FROM current_measurements WHERE cell_ID = 3") # ORDER BY ID DESC LIMIT 1
# cell3_values = mycursor.fetchall()
# last_value = cell3_values[-1]
# print(cell3_values)
# print(last_value)
# print(float(last_value[0]))
#cell_number = 1
# mycursor.execute("SELECT voltage FROM voltage_measurements WHERE module_ID = 1 AND cell_ID = "+ str(cell_number))
# data = mycursor.fetchall()
# last_value = data [-1]
# voltage = float (last_value[0])

# for x in myresult:
#   print(x)
# voltage = mycursor.fetchone()  # retrieve first row as a tuple 
# print((voltage[0]))
#****************************#
#mycursor.execute("SELECT SOC FROM cells_state_of_charge WHERE module_ID = 1 AND cell_ID = "+ str(cell_number)+ "ORDER BY ID DESC LIMIT 1")
# sql = "SELECT SOC FROM cells_state_of_charge WHERE module_ID = 1 AND cell_ID = "+ str(cell_number) + " ORDER BY ID DESC LIMIT 1"
# mycursor.execute(sql)
# data = mycursor.fetchone()
# return_value = data[0]
# # last_value = data [-1]
# # state_of_charge = float (last_value[0])
# print(  return_value)