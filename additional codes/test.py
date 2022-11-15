
from datetime import date
import time
while True:
 global num_of_cycles
 file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/num_of_cycles.txt", "r")   # open the file 'num_of_cycles.txt' in raeding mode.
 num_of_cycles = int (file.read())
 print (num_of_cycles)
 file.close() 

#  num_of_cycles += 1
 file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/num_of_cycles.txt", "w")
 file.truncate()      # delete the last value of number of cycles.
 num_of_cycles += 1
 file.write(str(num_of_cycles))
 file.close()
 time.sleep(2)
# file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/num_of_cycles.txt", "r")
# num_of_cycles = int (file.read())
# print (num_of_cycles)

# today = date.today()
# month_from_year = today.year - 2021
# global month_from_month
# month_from_month = today.month - 10
# global total_number_of_months
# total_number_of_months = 12      #* month_from_year + month_from_month     # get the total number of months.
# #print (total_number_of_months)

# def fun ():
#   global total_number_of_months
#   print (total_number_of_months)
#   total_number_of_months += 1
#   print(total_number_of_months)
  

# fun()

# def fun2 ():
#     global total_number_of_months
#     print(total_number_of_months)

# fun2 ()