

import numpy as np
from math import fabs

def rainflow_algorithm(DoD_array):
    
    num_DoD_array_elements = DoD_array.size                # total size of input array
    cycle_count_array = np.zeros((num_DoD_array_elements-1))    # initialize output array
    
    index__DoD_array = 0                                  # index of input array
    index_cycle_count_array = 0                           # index of output array
    j = -1                                  # index of temporary array "a"
    temporary_array  = np.empty(DoD_array.shape)          # temporary array for algorithm
    
    
    for i in range(num_DoD_array_elements):   # loop through each turning point stored in input array
        j += 1                  # increment temporary_array counter
        temporary_array[j] = DoD_array[index__DoD_array]    # put turning point into temporary array
        index__DoD_array += 1                 # increment input array pointer
        Rx = fabs( temporary_array[j-1] - temporary_array[j-2] )
        Ry= fabs( temporary_array[j] - temporary_array[j-1])
        while ((j >= 2) & ( Rx <= Ry ) ):      # Rx <= Ry
            DoD_range = fabs( temporary_array[j-1] - temporary_array[j-2] )
              
            # partial range
            if j == 2:
                temporary_array[0]=temporary_array[1]
                temporary_array[1]=temporary_array[2]
                j=1
                if (DoD_range > 0):
                    cycle_count_array[index_cycle_count_array] = 0.5
                    index_cycle_count_array += 1
                
            # full range
            elif j > 2:
                temporary_array[j-2]=temporary_array[j]
                j=j-2
                if (DoD_range > 0):
                    try:
                        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/num_of_cycles.txt", "r")
                        num_of_cycles = int (file.read())
                    finally:
                        file.close()
                    num_of_cycles += 1
                    try:
                        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/num_of_cycles.txt", "w")
                        file.truncate()      # delete the last value of number of cycles.
                        file.write(str(num_of_cycles))
                    finally:
                        file.close()
                    cycle_count_array[index_cycle_count_array] = 1.00
                    index_cycle_count_array += 1
                    
    # partial range
    for i in range(j):
        DoD_range    = fabs( temporary_array[i] - temporary_array[i+1] )

        if (DoD_range > 0):
            cycle_count_array[index_cycle_count_array] = 0.5
            index_cycle_count_array += 1  

    return cycle_count_array

def run():

    DoD_array = np.array([28,29,30,28,26,26.5,27,26,24,27,29,26,22,27,30])  # array of DoD points.
    cycle_count_array= rainflow_algorithm(DoD_array)
    print(cycle_count_array)

run()

# print(cycle_count_array[4])
# print(cycle_count_array[3:5])
# print(cycle_count_array)
