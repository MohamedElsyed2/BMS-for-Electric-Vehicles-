global num_of_cycles
num_of_cycles += 1
file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/num_of_cycles.txt", "w")
file.truncate()      # delete the last value of number of cycles.
file.write(str(num_of_cycles))
file.close()