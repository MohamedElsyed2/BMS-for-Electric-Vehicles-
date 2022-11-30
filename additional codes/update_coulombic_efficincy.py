
import time
import threading

def calibrate_cell1_coulombic_Efficiency(cell_number):
    global is_discharged_capacity_done
    is_discharged_capacity_done = False
    def get_discharged_capacity (cell_number):
        is_fully_charged = False
        discharged_capacity = 0
        charged_capacity = 0
        if cell_number < 5:
            number = str(cell_number)
            try:        
                file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+number+"_voltage.txt", "r")
                voltage = float (file.read())
            finally:
                file.close()
            try:        
                file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+number+"_current.txt", "r")
                current = float (file.read())
            finally:
                file.close()
        elif cell_number == 5:
            try:        
                file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_voltage.txt", "r")
                voltage = float (file.read())
            finally:
                file.close()
            try:        
                file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_current.txt", "r")
                current = float (file.read())
            finally:
                file.close()
        #*****************************************************************************#
        if voltage >= 4.2 and current >= -0.065:              # this meaning the battaery is fully charged.
            is_fully_charged = True
            
        while is_fully_charged and voltage > 2.5 :                       #and is_fully_discharged = False :
            try:        
                file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_current.txt", "r")
                current = float (file.read())
            finally:
                file.close()
            if current >= 0:            #  this means the battery is in discharging stage, then we can calculate the discharged capacity.
                discharged_capacity += current * (1/3600)  # time is 1 sec to converte it to hour, it os devided by 3600.
                time.sleep(1)
            else:                         #  this means the battery is in charging stage, then we can calculate the charged capacity.
                charged_capacity += abs(current) * (1/3600)  # time is 1 sec to converte it to hour, it os devided by 3600.
                time.sleep(1)
            try:        
                file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_voltage.txt", "r")
                voltage = float (file.read())
            finally:
                file.close()
            if voltage <= 2.5:     # this meaning the battaery is fully discharged.
                is_fully_charged = False
                global is_discharged_capacity_done
                is_discharged_capacity_done = True        # this meaning a dicharging cycle occured.
        discharged_capacity_oncycle = discharged_capacity - charged_capacity
        return discharged_capacity_oncycle
    #*****************************************************************#
    discharged_capacity = get_discharged_capacity (cell_number)
    if is_discharged_capacity_done == True:                 # if the discharged capacity be calculated, then update the coulombic_Efficiency.
        rated_capacity = 3.350            # Ah
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_state_of_health.txt", "r")  
        state_of_health = float (file.read())
        file.close()
        recalibrated_rated_capacity = rated_capacity * state_of_health
        error = recalibrated_rated_capacity - discharged_capacity
        try:
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_coulombic_efficiency.txt", "r")  
            old_coulombic_Efficiency = float (file.read())
        finally:
            file.close()
        try:        
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_coulombic_efficiency_numinator.txt", "r")
            coulombic_Efficiency_numinator = float (file.read())
        finally:
            file.close()
        try:        
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_coulombic_efficiency_denominator.txt", "r")
            coulombic_Efficiency_denominator = float (file.read())
        finally:
            file.close()
        coulombic_Efficiency_numinator += discharged_capacity *(old_coulombic_Efficiency * discharged_capacity + error)
        coulombic_Efficiency_denominator += pow(discharged_capacity,2)
        calibrated_coulombic_Efficiency = coulombic_Efficiency_numinator / coulombic_Efficiency_denominator
        try:
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_coulombic_efficiency.txt", "w")
            file.truncate()      
            file.write(str(calibrated_coulombic_Efficiency))
        finally:
            file.close()
        try:  # This way, we are guaranteeing that the file is properly closed even if an exception is raised that causes program flow to stop.
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_coulombic_efficiency_numinator.txt", "w")
            file.truncate()      
            file.write(str(coulombic_Efficiency_numinator))
        finally:
            file.close()  
        try:        
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_coulombic_efficiency_denominator.txt", "w")
            file.truncate()
            file.write(str(coulombic_Efficiency_denominator))
        finally:
            file.close()    

# while True:
#     calibrate_cell1_coulombic_Efficiency()

def run():
    while True:
        thread_1 = threading.Thread(target=calibrate_cell1_coulombic_Efficiency, args=(1,))
        thread_1.start()

run()
