
import time
from datetime import date

def get_state_of_health ():
    #******* Start of the code to calculate the effect of self-discharge on total sate of health of the battery*********#
    def SOH_self_discharge():
        today = date.today()
        month_from_year = today.year - 2022
        month_from_month = today.month - 8
        total_number_of_months = 12* month_from_year + month_from_month     # get the total number of months.
        if total_number_of_months <= 2:
            soc_self_discharge_coeff = 1
        elif total_number_of_months > 2 and total_number_of_months <= 6:
            soc_self_discharge_coeff = 0.95
        elif total_number_of_months > 6 and total_number_of_months <= 24:
            soc_self_discharge_coeff = 1 - (total_number_of_months/100)
        elif total_number_of_months > 24 and total_number_of_months <= 36:
            soc_self_discharge_coeff = 0.76 - 0.05 *(total_number_of_months - 24)
        elif total_number_of_months > 36 and total_number_of_months <= 96:
            soc_self_discharge_coeff = 0.7 - 0.025 *(total_number_of_months - 24)
        else:
            #client.publish(topic ="errors", payload= 5 , qos=1)
            soc_self_discharge_coeff = 0
        return soc_self_discharge_coeff
    #print (SOH_self_discharge())
#******* End of the code to calculate the effect of self-discharge on total sate of health of the battery********#
#******* Start of the code to calculate the effect of number of cycles on total sate of health of the battery*********#
    def SOH_num_of_cycles ():     # not complete
        global num_of_cycles
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/num_of_cycles.txt", "r")   # open the file 'num_of_cycles.txt' in raeding mode.
        num_of_cycles = int (file.read())
        file.close() 
        global soc_num_of_cycles_coeff
        if num_of_cycles <= 100:
            soc_num_of_cycles_coeff = 1
        elif num_of_cycles > 100 and num_of_cycles <= 200:
            soc_num_of_cycles_coeff = 0.95
        elif num_of_cycles > 200 and num_of_cycles <= 500:
            soc_num_of_cycles_coeff = 0.85
        else:
            soc_num_of_cycles_coeff = 0.85
        return soc_num_of_cycles_coeff

    total_SOH = SOH_self_discharge() * SOH_num_of_cycles ()
    return total_SOH
#******* End of the code to calculate the effect of number of cycles on total sate of health of the battery*********#
    
def run():
    while True:
        total_SOH  = int (100000*get_state_of_health ())
        true_SOH = total_SOH/1000
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell1_state_of_health.txt", "w")
        file.truncate()       # delete the last value of number of cycles.
        file.write(str(true_SOH))
        file.close()
        print("Cell_1 SOH= ",true_SOH,"% \n")
        time.sleep(2)
        #client.publish(topic ="SOH_cell1", payload= str(SOH) , qos=1)        #client.publish(topic ="SOH_cell1", payload= str(SOH) , qos=1)

#run()
