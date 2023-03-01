
import time
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

def timer ():
    #while True:
        print("standalone timer is running")
        # file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/timer.txt", "r")  
        # timer_1 = int (file.read())
        # file.close()
        sql = "SELECT timer_value FROM timer ORDER BY ID DESC LIMIT 1"
        mycursor.execute(sql)
        data = mycursor.fetchone()
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
        mycursor.execute(sql , values) # store the measurement value in SQL database
        mydb.commit()  # Commit the transaction
        time.sleep(60)                    # wait for 60 seconds.
        

def run():
    timer()
    
#run()