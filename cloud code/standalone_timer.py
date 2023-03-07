
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
mutex=threading.Lock() # craete a lock fot the threads


def timer ():
    
    while True:
        # file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/timer.txt", "r")  
        # timer_1 = int (file.read())
        # file.close()
        sql = "SELECT timer_value FROM timer ORDER BY ID DESC LIMIT 1"
        mutex.acquire()
        mycursor.execute(sql)
        data = mycursor.fetchone()
        mutex.release()
        timer_1 = data[0]

        if timer_1 >= 4294967295:               # to prevent the timer from overflow.
            timer_1 = 1
        else:
            timer_1 += 1
        # file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/timer.txt", "w")
        # file.truncate()       # delete the last value of number of cycles.
        # file.write(str(timer_1))
        # file.close()
        sql = "INSERT INTO timer (timer_value) VALUES (%s)"
        values = (timer_1,)
        mutex.acquire()
        mycursor.execute(sql , values) # store the measurement value in SQL database
        mydb.commit()  # Commit the transaction
        mutex.release()
        time.sleep(60)                    # wait for 60 seconds.
        

def run():
    print("standalone timer is running")
    timer()
    
#run()