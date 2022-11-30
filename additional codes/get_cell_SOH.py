def fun(cell_number):
    if cell_number == 1:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_state_of_health.txt", "r")  
        state_of_health = float (file.read())
        file.close()
    elif cell_number == 2:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell2_state_of_health.txt", "r")  
        state_of_health = float (file.read())
        file.close()
    elif cell_number == 3:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell3_state_of_health.txt", "r")  
        state_of_health = float (file.read())
        file.close()
    elif cell_number == 4:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell4_state_of_health.txt", "r")  
        state_of_health = float (file.read())
        file.close()
    elif cell_number == 5:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_state_of_health.txt", "r")  
        state_of_health = float (file.read())
        file.close()
    return state_of_health

print(fun(5))