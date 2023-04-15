
import time
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

sql = "SELECT temperature FROM modules_temperature WHERE module_ID = 1 ORDER BY ID DESC LIMIT 1"
mutex.acquire()
mycursor.execute(sql)
data = mycursor.fetchone()
mutex.release()
temperature = data[0]

cooling_sys_status = 0
heating_sys_status = 0
print("thermal management is running")
def run():
    
    global cooling_sys_status
    global heating_sys_status
    if temperature > 25:
       
        cooling_sys_status = 1
        heating_sys_status = 0
    elif temperature < 25:
        
        heating_sys_status = 1
        cooling_sys_status = 0
    else:
       
        cooling_sys_status = 0
        heating_sys_status = 0
    
    sql = "INSERT INTO thermal_manag_sys (cooling_sys_status, heating_sys_status) VALUES (%s, %s)" # store the ststus of the cooling and heating systems.
    values = (cooling_sys_status, heating_sys_status)
    mutex.acquire()
    mycursor.execute(sql , values) # store the measurement value in SQL database
    mydb.commit()  # Commit the transaction
    mutex.release()
    time.sleep(60)
#run()