# file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/soc_calibration.txt", "r")   # open the file 'temperature.txt' in raeding mode.
# is_int_soc_calibration_done = file.read()
# file.close() 
# if eval(is_int_soc_calibration_done) == True:
#     print("true")
# else:
#     print("false")
import numpy
timmer_interrupt = 4294967295
if timmer_interrupt % 5 == 0:
    print("yes")
else:
    print("no")