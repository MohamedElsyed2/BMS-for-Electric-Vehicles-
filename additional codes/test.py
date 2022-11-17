
# # from datetime import date
# # import time
# # while True:
# #  global num_of_cycles
# #  file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/num_of_cycles.txt", "r")   # open the file 'num_of_cycles.txt' in raeding mode.
# #  num_of_cycles = int (file.read())
# #  print (num_of_cycles)
# #  file.close() 

# # #  num_of_cycles += 1
# #  file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/num_of_cycles.txt", "w")
# #  file.truncate()      # delete the last value of number of cycles.
# #  num_of_cycles += 1
# #  file.write(str(num_of_cycles))
# #  file.close()
# #  time.sleep(2)
# # file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/num_of_cycles.txt", "r")
# # num_of_cycles = int (file.read())
# # print (num_of_cycles)

# # today = date.today()
# # month_from_year = today.year - 2021
# # global month_from_month
# # month_from_month = today.month - 10
# # global total_number_of_months
# # total_number_of_months = 12      #* month_from_year + month_from_month     # get the total number of months.
# # #print (total_number_of_months)

# # def fun ():
# #   global total_number_of_months
# #   print (total_number_of_months)
# #   total_number_of_months += 1
# print(pow(3,2))
# print(3**2)

# def measuere ():
#     #**********************************************************#
#     global temperature
#     temperature = 30
#     #************************* Start of battery_age_estimation method*****************************************#
#     def battery_age_estimation ():
#         #******************* Start of battery_age_temperature method***********************************#
#         def battery_age_temperature():
#             global temperature                   # the real temperature of the battery cell.
#             a = 0.0039
#             b = 1.95
#             c = 67.51
#             d = 2070
#             nominal_temperature = 25
#             num_cycle_life_temp = (a*pow(temperature,3) - b*pow(temperature,2) + c*temperature + d)/(a*pow(nominal_temperature,3) - b*pow(nominal_temperature,2) + c*nominal_temperature + d)
#             return num_cycle_life_temp
#         #******************* End of battery_age_temperature method***********************************#
#         #******************* Start of battery_age_disch_current method*******************************#
#         def battery_age_disch_current():
#             num_cycle_life_disch_current = 2
#             return num_cycle_life_disch_current
#         #******************* End of battery_age_disch_current method*******************************#
#         equivelant_battery_num_cycle_life = battery_age_temperature() * battery_age_disch_current()
#         return equivelant_battery_num_cycle_life
#     #************************* End of battery_age_estimation method*****************************************#
#     print (battery_age_estimation ())
# from math import exp
# print (exp(0))

# import time
# from threading import Thread


# class Worker(Thread):
#     def run(self):
#         for x in range(0, 11):
#             print(x)
#             time.sleep(1)

# print("Staring Worker Thread")
# Worker().start()
# class Waiter(Thread):
#     def run(self):
#         for x in range(100, 103):
#             print(x)
#             time.sleep(5)

import threading
import time


def print_hello():
    global current
    current = 5
    time.sleep(1)
    current = 4
    #return current
thread_1 = threading.Thread(target=print_hello())
thread_1.start()

def print_hi():
    global voltage
    voltage= 3
    time.sleep(2)
    voltage = 5
    return voltage

# print(time.localtime())
thread_2 = threading.Thread(target=print_hi)  
thread_2.start()
#print_hello()
#print_hi()
print(current * print_hi() )
#print(time.localtime())

# print(time.localtime())
# import array
# import time
# global tem 
# tem = 5
# clT_array = array.array('f', [])                  # clT_array: is the array of cycle life of temperature, 'f': stands for float.
# for i in range (0,4):
#                 num_cycle_life_temp = tem
#                 clT_array.append (num_cycle_life_temp)       # adding an num_cycle_life_temp to the array.
#                 time.sleep(1)                              # wait for 6 hours to get another value of num_cycle_life_temp.
# avr_num_cycle_life_temp= (clT_array[0]+clT_array[1]+clT_array[2]+clT_array[3])/4
# print(clT_array)
# print(avr_num_cycle_life_temp)
# print(time.)

#global a 
# a= 5
# def func():
#  def fun3():
#     def fun2():
#         global a
#         a += 1
#     fun2()
#  fun3()
# func()
# def fun5():
#     global a
#     a = 10
# fun5()
# print(a)