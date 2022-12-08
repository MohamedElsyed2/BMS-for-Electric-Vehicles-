from numpy import fabs
import numpy as np


DoD_array = np.array([28,29,30,28,26,26.5,27,26,24,27,29,26,22,27,30])  # array of DoD points.
num_DoD_array_elements = DoD_array.size
#print(num_DoD_array_elements)

array_out = np.zeros(( num_DoD_array_elements-1)) 
temporary_array  = np.empty(DoD_array.shape) 
#print(array_out)

print(temporary_array)