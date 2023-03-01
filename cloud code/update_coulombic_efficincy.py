
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
print("Thread4!")
def calibrate_cell1_coulombic_Efficiency(cell_number):
    while True:
        print("update coulombic efficincy is running")
        time.sleep(2)
        global is_discharged_capacity_done
        is_discharged_capacity_done = False 
        def get_discharged_capacity (cell_number):
            is_fully_charged = False
            discharged_capacity = 0
            charged_capacity = 0
            if cell_number < 4:
                #number = str(cell_number)
                # try:        
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+number+"_voltage.txt", "r")
                #     voltage = float (file.read())
                # finally:
                #     file.close()
                sql = "SELECT voltage FROM voltage_measurements WHERE module_ID = 1 AND cell_ID = "+str(cell_number)+" ORDER BY ID DESC LIMIT 1"
                mycursor.execute(sql)
                data = mycursor.fetchone()
                voltage = data[0]
                # try:        
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+number+"_current.txt", "r")
                #     current = float (file.read())
                # finally:
                #     file.close()
                sql = "SELECT current FROM current_measurements WHERE module_ID = 1 AND cell_ID = "+str(cell_number)+" ORDER BY ID DESC LIMIT 1"
                mycursor.execute(sql)
                data = mycursor.fetchone()
                current = data[0]

            elif cell_number == 4:            # in case of the whole module number 1.
                # try:        
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_voltage.txt", "r")
                #     voltage = float (file.read())
                # finally:
                #     file.close()
                sql = "SELECT voltage FROM modules_voltage WHERE module_ID = 1 ORDER BY ID DESC LIMIT 1"
                mycursor.execute(sql)
                data = mycursor.fetchone()
                voltage = data[0]

                # try:        
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_current.txt", "r")
                #     current = float (file.read())
                # finally:
                #     file.close()
                sql = "SELECT current FROM modules_current WHERE module_ID = 1 ORDER BY ID DESC LIMIT 1"
                mycursor.execute(sql)
                data = mycursor.fetchone()
                current = data[0]
            #*****************************************************************************#
            if voltage >= 4.2 and current >= -0.065:              # this meaning the battaery is fully charged.
                is_fully_charged = True
                
            while is_fully_charged and voltage > 2.5 :                       #and is_fully_discharged = False :
                #****************************************************************#
                if cell_number < 4:
                    #number = str(cell_number)
                    # try:        
                    #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+number+"_voltage.txt", "r")
                    #     voltage = float (file.read())
                    # finally:
                    #     file.close()
                    sql = "SELECT voltage FROM voltage_measurements WHERE module_ID = 1 AND cell_ID = "+str(cell_number)+" ORDER BY ID DESC LIMIT 1"
                    mycursor.execute(sql)
                    data = mycursor.fetchone()
                    voltage = data[0]
                    # try:        
                    #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+number+"_current.txt", "r")
                    #     current = float (file.read())
                    # finally:
                    #     file.close()
                    sql = "SELECT current FROM current_measurements WHERE module_ID = 1 AND cell_ID = "+str(cell_number)+" ORDER BY ID DESC LIMIT 1"
                    mycursor.execute(sql)
                    data = mycursor.fetchone()
                    current = data[0]
                elif cell_number == 4:            # in case of the whole module number 1.
                    # try:        
                    #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_voltage.txt", "r")
                    #     voltage = float (file.read())
                    # finally:
                    #     file.close()
                    sql = "SELECT voltage FROM modules_voltage WHERE module_ID = 1 ORDER BY ID DESC LIMIT 1"
                    mycursor.execute(sql)
                    data = mycursor.fetchone()
                    voltage = data[0]
                    # try:        
                    #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_current.txt", "r")
                    #     current = float (file.read())
                    # finally:
                    #     file.close()
                    sql = "SELECT current FROM modules_current WHERE module_ID = 1 ORDER BY ID DESC LIMIT 1"
                    mycursor.execute(sql)
                    data = mycursor.fetchone()
                    current = data[0]
            #***************************************************#
                if current >= 0:            #  this means the battery is in discharging stage, then we can calculate the discharged capacity.
                    discharged_capacity += current * (10/3600)  # time is 1 sec to converte it to hour, it os devided by 3600.
                    time.sleep(10)
                else:                         #  this means the battery is in charging stage, then we can calculate the charged capacity.
                    charged_capacity += abs(current) * (1/3600)  # time is 1 sec to converte it to hour, it os devided by 3600.
                    time.sleep(10)
                
                if voltage <= 2.5:     # this meaning the battaery is fully discharged.
                    is_fully_charged = False
                    global is_discharged_capacity_done
                    is_discharged_capacity_done = True        # this meaning a dicharging cycle occured.
            discharged_capacity_oncycle = discharged_capacity - charged_capacity
            return discharged_capacity_oncycle
        #*****************************************************************#
        ######################## start get SOH *****************************#
        def get_state_of_health (cell_number):
            if cell_number < 4:
                #number = str(cell_number)
                # file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+number+"_state_of_health.txt", "r")  
                # state_of_health = float (file.read())
                # file.close()
                sql = "SELECT SOH FROM cells_state_of_health WHERE module_ID = 1 AND cell_ID = "+ str(cell_number) +" ORDER BY ID DESC LIMIT 1"
                mycursor.execute(sql)
                data = mycursor.fetchone()
                state_of_health = data[0]
            elif cell_number == 4:
                # file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_state_of_health.txt", "r")  
                # state_of_health = float (file.read())
                # file.close()
                sql = "SELECT SOH FROM modules_state_of_health WHERE module_ID = 1 " 
                mycursor.execute(sql)
                data = mycursor.fetchone()
                state_of_health = data[0]
            return state_of_health
        #************************ End get SOH ******************************#
        #************************ Start get old_coulombic_Efficiency **********#
        def get_old_coulombic_Efficiency(cell_number):
            if cell_number < 4:
                number = str(cell_number)
                # file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+number+"_coulombic_efficiency.txt", "r")  
                # old_coulombic_Efficiency = float (file.read())
                # file.close()
                sql= "SELECT coulombic_efficiency FROM cells_coulombic_efficiency WHERE module_ID = 1 AND cell_ID = "+ str(cell_number)+" ORDER BY ID DESC LIMIT 1"
                mycursor.execute(sql)
                data = mycursor.fetchone()
                old_coulombic_Efficiency = data[0]
            elif cell_number == 4:
                # file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_coulombic_efficiency.txt", "r")  
                # old_coulombic_Efficiency = float (file.read())
                # file.close()
                sql= "SELECT coulombic_efficiency FROM modules_coulombic_efficiency WHERE module_ID = 1"
                mycursor.execute(sql)
                data = mycursor.fetchone()
                old_coulombic_Efficiency = data[0]
            return old_coulombic_Efficiency
        #************************ End get old_coulombic_Efficiency **********#
        #*********************** Start get_coulombic_Efficiency_numinator ************#
        def get_coulombic_Efficiency_numinator(cell_number):
            if cell_number < 4:
                #number = str(cell_number)
                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+number+"_coulombic_efficiency_numinator.txt", "r")  
                #     coulombic_Efficiency_numinator = float (file.read())
                # finally:
                #     file.close()
                sql= "SELECT coulombic_Efficiency_numinator FROM cells_coulombic_Efficiency_numinator WHERE module_ID = 1 AND cell_ID = "+ str(cell_number)+" ORDER BY ID DESC LIMIT 1"
                mycursor.execute(sql)
                data = mycursor.fetchone()
                coulombic_Efficiency_numinator = data[0]
            elif cell_number == 4:
                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_coulombic_efficiency_numinator.txt", "r")  
                #     coulombic_Efficiency_numinator = float (file.read())
                # finally:
                #     file.close()
                sql= "SELECT coulombic_Efficiency_numinator FROM modules_coulombic_Efficiency_numinator WHERE module_ID = 1"
                mycursor.execute(sql)
                data = mycursor.fetchone()
                coulombic_Efficiency_numinator = data[0]
            return coulombic_Efficiency_numinator
        #*********************** End get_coulombic_Efficiency_numinator ************#
        #*********************** Start get_coulombic_Efficiency_denominator ************#
        def get_coulombic_Efficiency_denominator(cell_number):
            if cell_number < 4:
                #number = str(cell_number)
                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+number+"_coulombic_efficiency_denominator.txt", "r")  
                #     coulombic_Efficiency_denominator = float (file.read())
                # finally:
                #     file.close()
                sql= "SELECT coulombic_Efficiency_denominator FROM cells_coulombic_Efficiency_denominator WHERE module_ID = 1 AND cell_ID = "+ str(cell_number)+" ORDER BY ID DESC LIMIT 1"
                mycursor.execute(sql)
                data = mycursor.fetchone()
                coulombic_Efficiency_denominator = data[0]
            elif cell_number == 4:
                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_coulombic_efficiency_denominator.txt", "r")  
                #     coulombic_Efficiency_denominator = float (file.read())
                # finally:
                #     file.close()
                sql= "SELECT coulombic_Efficiency_denominator FROM modules_coulombic_Efficiency_denominator WHERE module_ID = 1 ORDER BY ID DESC LIMIT 1"
                mycursor.execute(sql)
                data = mycursor.fetchone()
                coulombic_Efficiency_denominator = data[0]
            return coulombic_Efficiency_denominator
        #*********************** End get_coulombic_Efficiency_denominator ************#
        #*********************** Start write the new values  *************************#
        def write_updated_coulombic_Efficiency (cell_number, calibrated_coulombic_Efficiency, coulombic_Efficiency_numinator, coulombic_Efficiency_denominator):
            if cell_number < 4:
                number = str(cell_number)
                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+number+"_coulombic_efficiency.txt", "w")  
                #     file.truncate()
                #     file.write(str(calibrated_coulombic_Efficiency))
                # finally:
                #     file.close()
                sql = "INSERT INTO cells_coulombic_efficiency (module_ID,cell_ID, coulombic_efficiency) VALUES (%s, %s, %s)"
                values = (1,cell_number, calibrated_coulombic_Efficiency)
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()  # Commit the transaction
                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+number+"_coulombic_efficiency_numinator.txt", "w")  
                #     file.truncate()
                #     file.write(str(coulombic_Efficiency_numinator))
                # finally:
                #     file.close()
                sql = "INSERT INTO cells_coulombic_Efficiency_numinator (module_ID,cell_ID, coulombic_Efficiency_numinator) VALUES (%s, %s, %s)"
                values = (1,cell_number, coulombic_Efficiency_numinator)
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()  # Commit the transaction

                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+number+"_coulombic_efficiency_denominator.txt", "w")  
                #     file.truncate()
                #     file.write(str(coulombic_Efficiency_denominator))
                # finally:
                #     file.close()
                sql = "INSERT INTO cells_coulombic_Efficiency_denominator (module_ID,cell_ID, coulombic_Efficiency_denominator) VALUES (%s, %s, %s)"
                values = (1,cell_number, coulombic_Efficiency_denominator)
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()  # Commit the transaction


            elif cell_number == 4:        # in case of module 1.
                # try:
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_coulombic_efficiency.txt", "w")
                #     file.truncate()      
                #     file.write(str(calibrated_coulombic_Efficiency))
                # finally:
                #     file.close()
                sql = "INSERT INTO modules_coulombic_efficiency (module_ID, coulombic_efficiency) VALUES (%s, %s)"
                values = (1, calibrated_coulombic_Efficiency)
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()  # Commit the transaction
                # try:  # This way, we are guaranteeing that the file is properly closed even if an exception is raised that causes program flow to stop.
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_coulombic_efficiency_numinator.txt", "w")
                #     file.truncate()      
                #     file.write(str(coulombic_Efficiency_numinator))
                # finally:
                #     file.close()
                sql = "INSERT INTO modules_coulombic_Efficiency_numinator (module_ID, coulombic_Efficiency_numinator) VALUES (%s, %s)"
                values = (1, coulombic_Efficiency_numinator)
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()  # Commit the transaction
                # try:        
                #     file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_coulombic_efficiency_denominator.txt", "w")
                #     file.truncate()
                #     file.write(str(coulombic_Efficiency_denominator))
                # finally:
                #     file.close() 
                sql = "INSERT INTO modules_coulombic_Efficiency_denominator (module_ID, coulombic_Efficiency_denominator) VALUES (%s, %s)"
                values = (1, coulombic_Efficiency_denominator)
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()  # Commit the transaction

        #*********************** End write the new values  *************************#
        discharged_capacity = get_discharged_capacity (cell_number)
        if is_discharged_capacity_done == True:                 # if the discharged capacity be calculated, then update the coulombic_Efficiency.
            if cell_number < 4:
                rated_capacity = 3.350                                         # rated capacity (Ah) at 25° C
            elif cell_number == 4:
                rated_capacity = 10050          
            recalibrated_rated_capacity = rated_capacity * get_state_of_health (cell_number)
            error = recalibrated_rated_capacity - discharged_capacity
            old_coulombic_Efficiency = get_old_coulombic_Efficiency(cell_number)
            coulombic_Efficiency_numinator = get_coulombic_Efficiency_numinator(cell_number)
            coulombic_Efficiency_denominator = get_coulombic_Efficiency_denominator(cell_number)

            coulombic_Efficiency_numinator += discharged_capacity *(old_coulombic_Efficiency * discharged_capacity + error)
            coulombic_Efficiency_denominator += pow(discharged_capacity,2)
            calibrated_coulombic_Efficiency = coulombic_Efficiency_numinator / coulombic_Efficiency_denominator

            #### update the old values with the new ones.
            write_updated_coulombic_Efficiency (cell_number,calibrated_coulombic_Efficiency,coulombic_Efficiency_numinator,coulombic_Efficiency_denominator)


def run():

    # thread_1 = threading.Thread(target=calibrate_cell1_coulombic_Efficiency, args=(1,))
    # thread_2 = threading.Thread(target=calibrate_cell1_coulombic_Efficiency, args=(2,))
    # thread_3 = threading.Thread(target=calibrate_cell1_coulombic_Efficiency, args=(3,))
    # thread_4 = threading.Thread(target=calibrate_cell1_coulombic_Efficiency, args=(4,))
    
    # thread_1.start()
    # thread_2.start()
    # thread_3.start()
    # thread_4.start()
    # thread_1.join()   # wait until thread 1 is completely executed
    # thread_2.join()
    # thread_3.join()
    # thread_4.join()
    # thread_5.join()
    #while True:
        for i in range(4):
            calibrate_cell1_coulombic_Efficiency(i+1)
    
#run()
