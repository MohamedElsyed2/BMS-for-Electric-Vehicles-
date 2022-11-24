# # file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/soc_calibration.txt", "r")   # open the file 'temperature.txt' in raeding mode.
# # is_int_soc_calibration_done = file.read()
# # file.close() 
# # if eval(is_int_soc_calibration_done) == True:
# #     print("true")
# # else:
# #     print("false")
# import numpy
# timmer_interrupt = 4294967295
# if timmer_interrupt % 5 == 0:
#     print("yes")
# else:
#     print("no")
voltage = 3.715 #3.85
rated_capacity= 3350
if voltage >= 3.84 and voltage < 4.2 :                     # from the battery datasheet, according to Charge Characteristics for NCR18650B1S.
    residual_capacity = 3570 *(voltage-3.375)  
elif voltage >= 3.54 and voltage < 3.84 :
    residual_capacity = 5040 *(voltage-3.516)         
elif voltage >= 3.3 and voltage < 3.54 :
    residual_capacity = 450 *(voltage-3.3)    
elif voltage < 3.3:        
    socIntial=0
socIntial= residual_capacity/ rated_capacity

print (residual_capacity)