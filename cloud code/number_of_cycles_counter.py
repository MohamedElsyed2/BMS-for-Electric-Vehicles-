

import numpy as np
from math import fabs
import time
import threading
print("Thread8!")
""" These methods are coded according to the methodology and  explanation of Rainflow counting method which is published in: 
Alam, M. J. E., and T. K. Saha. "Cycle-life degradation assessment of Battery Energy Storage Systems caused by solar PV variability.
" In 2016 IEEE Power and Energy Society General Meeting (PESGM), pp. 2. IEEE, 2016."""


def rainflow_algorithm(cell_number):
    while True:
        print("cycles counter is running")
        #time.sleep(2)
        #**************************** Start of get the depth of discharging array *************#
        def get_DoD_array(cell_number):
            #DoD_array =np.array([0,10,5,2,3,10,10,0,0,30,15,10,20,10,0,0,0,0,0,0,0,15,10,10,5,10,10,0,0,10,10,0,0,0,0,25,35,0,0,20,40,0,0,0,0,0,0,0,0,0,0]) # array of DoD points.
            DoD_array =np.zeros(48)         # intialize an array of zeros with size 48.
            counter = 0
            while counter < 48:
                try:
                    file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_state_of_charge.txt", "r")
                    SoC_before = float (file.read())
                finally:
                    file.close()
                time.sleep (1800)  # 1800  # wait for half hour.
                try:
                    file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_state_of_charge.txt", "r")
                    SoC_after = float (file.read())
                finally:
                    file.close()
                diff_SoC = SoC_before - SoC_after

                if diff_SoC < 0:                  # in charging stage.
                    DoD = 0
                else:                             # discharging stage.
                    DoD = diff_SoC
                DoD_array [counter] = DoD

                counter += 1
            return DoD_array
        DoD_array = get_DoD_array(cell_number)
        #**************************** End of get the depth of discharging array *************#
        #**************************** Start Rainflow algorithm *************#
        num_DoD_array_elements = DoD_array.size                              # total size of deapth of discharge array
        cycle_count_array = np.zeros((num_DoD_array_elements-1))             # initialize cycles counter array
        
        index__DoD_array = 0                                           # index of eapth of discharge array
        index_cycle_count_array = 0                                      # index of ycles counter array
        j = -1                                                    # index of temporary array
        temporary_array  = np.empty(DoD_array.shape)              # temporary array, it is an array used in algorithm.
        
        
        for i in range(num_DoD_array_elements):                 # loop through each turning point stored in eapth of discharge array
            j += 1                                                    # increment temporary_array counter
            temporary_array[j] = DoD_array[index__DoD_array]          # put data point into temporary array
            index__DoD_array += 1                                    # increment eapth of discharge array index
            Rx = fabs( temporary_array[j-1] - temporary_array[j-2] )
            Ry= fabs( temporary_array[j] - temporary_array[j-1])
            while ((j >= 2) & ( Rx <= Ry ) ):      # Rx <= Ry
                DoD_range = fabs( temporary_array[j-1] - temporary_array[j-2] )
                
                
                if j == 2:
                    temporary_array[0]=temporary_array[1]
                    temporary_array[1]=temporary_array[2]
                    j=1
                    if (DoD_range > 0):
                        cycle_count_array[index_cycle_count_array] = 0.5
                        index_cycle_count_array += 1
                    
                elif j > 2:
                    temporary_array[j-2]=temporary_array[j]
                    j=j-2
                    if (DoD_range > 0):
                        try:
                            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_num_of_cycles.txt", "r")
                            num_of_cycles = int (file.read())
                        finally:
                            file.close()
                        num_of_cycles += 1
                        try:
                            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/cell"+str(cell_number)+"_num_of_cycles.txt", "w")
                            file.truncate()      # delete the last value of number of cycles.
                            file.write(str(num_of_cycles))
                        finally:
                            file.close()
                        cycle_count_array[index_cycle_count_array] = 1.00
                        index_cycle_count_array += 1
                        
        for i in range(j):
            DoD_range    = fabs( temporary_array[i] - temporary_array[i+1] )

            if (DoD_range > 0):
                cycle_count_array[index_cycle_count_array] = 0.5
                index_cycle_count_array += 1  

        #return cycle_count_array

def run():
    t_1 = threading.Thread(target=rainflow_algorithm, args=(1,))   # count the numer of cycles for cell1.
    t_2 = threading.Thread(target=rainflow_algorithm, args=(2,))   # count the numer of cycles for cell2.
    t_3 = threading.Thread(target=rainflow_algorithm, args=(3,))   # count the numer of cycles for cell3.
    t_1.start()
    t_2.start()
    t_3.start()
   
#run()

