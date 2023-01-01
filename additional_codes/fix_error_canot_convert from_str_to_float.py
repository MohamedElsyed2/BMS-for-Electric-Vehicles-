

import time
import os


try:
    file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_current.txt", "r")
    if os.stat("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_current.txt").st_size != 0:
        current = float (file.read())
    else:
        while os.stat("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_current.txt").st_size == 0:
            time.sleep(0.3)
            if os.stat("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_current.txt").st_size != 0:
                current = float (file.read())
finally:
    file.close()
#print("{} is empety".format(a))
print(current)
time.sleep(1)


# import time
# import os

# #True
# while True:
#     try:
#         file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_current.txt", "r")  
#         current = float (file.read())
#     except:
#         while os.stat("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_current.txt").st_size == 0:
#             time.sleep(0.3)
#             if os.stat("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_current.txt").st_size != 0:
#                 current = float (file.read())
#     finally:
#         file.close()
#     #print("{} is empety".format(a))
#     print(current)
#     time.sleep(1)