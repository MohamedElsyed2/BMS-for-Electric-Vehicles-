
from paho.mqtt import client
from datetime import date
global num_of_cycles
num_of_cycles = 0

#******* Start of the code to calculate the total sate of health of the battery*********#
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
    print (SOH_self_discharge())
    #******* End of the code to calculate the effect of self-discharge on total sate of health of the battery********#
    #******* Start of the code to calculate the effect of number of cycles on total sate of health of the battery*********#
    def SOH_num_of_cycles ():
        if num_of_cycles <= 100:
            soc_num_of_cycles_coeff = 1
        elif num_of_cycles > 100 and num_of_cycles <= 200:
            soc_num_of_cycles_coeff = 0.95
        
        return soc_num_of_cycles_coeff
    total_SOH = SOH_self_discharge() * SOH_num_of_cycles ()
    return total_SOH
SOH  = int (100000*get_state_of_health ())
print (SOH)
#client.publish(topic ="SOH_cell1", payload= str(SOH) , qos=1)
 #******* End of the code to calculate the effect of number of cycles on total sate of health of the battery*********#




        # elif total_number_of_months > 48 and total_number_of_months >= 60:
        #     soc_self_discharge_coeff = 0.65
        # elif total_number_of_months > 60 and total_number_of_months >= 72:
        #     soc_self_discharge_coeff = 0.6
        # elif total_number_of_months > 12 and total_number_of_months >= 14:
        #     soc_self_discharge_coeff = 0.88
        # elif total_number_of_months > 14 and total_number_of_months >= 16:
        #     soc_self_discharge_coeff = 0.86
        # elif total_number_of_months > 16 and total_number_of_months >= 18:
        #     soc_self_discharge_coeff = 0.84
        # elif total_number_of_months > 18 and total_number_of_months >= 20:
        #     soc_self_discharge_coeff = 0.82
        # elif total_number_of_months > 20 and total_number_of_months >= 22:
        #     soc_self_discharge_coeff = 0.8
        # elif total_number_of_months > 22 and total_number_of_months >= 24:
        #     soc_self_discharge_coeff = 0.78
        # elif total_number_of_months > 24 and total_number_of_months >= 26 :
        #     soc_self_discharge_coeff = 0.77
        # elif total_number_of_months > 26 and total_number_of_months >= 28:
        #     soc_self_discharge_coeff = 0.76
        # elif total_number_of_months > 28 and total_number_of_months >= 30:
        #     soc_self_discharge_coeff = 0.75
        # elif total_number_of_months > 30 and total_number_of_months >= 32:
        #     soc_self_discharge_coeff = 0.74
        



# a = 12 - today.month
# print("Current day:",a )

