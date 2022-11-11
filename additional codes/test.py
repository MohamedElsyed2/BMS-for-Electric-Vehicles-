
from datetime import date
today = date.today()
month_from_year = today.year - 2021
global month_from_month
month_from_month = today.month - 10
global total_number_of_months
total_number_of_months = 12      #* month_from_year + month_from_month     # get the total number of months.
#print (total_number_of_months)

def fun ():
  global total_number_of_months
  print (total_number_of_months)
  total_number_of_months += 1
  print(total_number_of_months)
  

fun()

def fun2 ():
    global total_number_of_months
    print(total_number_of_months)

fun2 ()