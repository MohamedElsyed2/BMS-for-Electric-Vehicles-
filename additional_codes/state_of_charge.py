
import time
global  cell1_voltage
cell1_voltage = 0
global cell1_current
cell1_current = 0
global temperature   # °C
temperature = 30
int_soc_flag= False
def func():
    
    
    def run2():
        a=2
        b=3
        c=4
        if c==4:
            global  cell1_voltage
            cell1_voltage=0.7    # (V)
        if a==2:
            global cell1_current
            cell1_current = 1.35  # (A)
        if b==3:
            global temperature   # °C
            temperature = 30
        
        
        
      #print (cell1_voltage)
    run2()
    # global cell1_Voltage
    # cell1_Voltage = cell1_voltage
    # global cell1_Current
    # cell1_Current = cell1_current
    # global battery_Temp
    # battery_Temp = temperature
 
#******************************************************************#
def get_thermal_coefficient(temperature):
    if temperature <= 25:
        thermal_coefficient=1
    elif temperature > 25 and temperature <= 50 :
        thermal_coefficient=0.95
    elif temperature > 50 and temperature <= 80 :
        thermal_coefficient=0.75
    else :
        thermal_coefficient=0.55
    return thermal_coefficient


#***************************************************************#
def get_soc_ocv (ocv):         # function to get the intial SOC of  from the relation between SOC and open circuit voltage (OCV).

    if ocv <= 0.5:
        socIntial=0
    elif ocv >0.5 and ocv <= 0.6 :
        socIntial= 0.05
    elif ocv >0.6 and ocv <= 0.75 :
        socIntial= 0.1 
    return socIntial

#******************************************************************#
def soc(cell_current,cell_voltage,temperature):

    max_cell_capacity = 0.6         # 600 mAh=0.6 Ah max cell capacity != the rated cell capacity, the rated cell capacity in this project = 600 mAh, if the battery is new, then the max cell capacity = rated cell capacity
    time_two_readings = 5 
    current = cell_current
    global state_of_charge
   
    global int_soc_flag
    if int_soc_flag == False:
       state_of_charge= get_soc_ocv (cell_voltage)           # get intial SOC from the open circuit voltage curve.
       int_soc_flag = True
    thermal_coefficient = get_thermal_coefficient (temperature)
    state_of_charge = state_of_charge + current* time_two_readings/3600*thermal_coefficient/ max_cell_capacity   #/3600 to convert from second to hour.
    time.sleep (2)                     # to wait 5 seconds between readings.
    return state_of_charge
#************************************************************************#
def runall():
 
 while True:
  func()
  cell1_state_of_charge= soc(cell1_current,cell1_voltage,temperature)
  print(100*cell1_state_of_charge,"% \n")
  print(cell1_current)


if __name__ == '__main__':
    runall()