import time
def run1():
    def run2():
      global  cell1_voltage
      global cell1_current
      global temperature
      cell1_voltage=0.7
      cell1_current = 1.35
      temperature = 30
      print (cell1_voltage)
    run2()
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
    total_cell_capacity = 3000         # cell capacity= 3000 mAh
    time_two_readings = 5 
    current = cell_current
    global state_of_charge
    state_of_charge= get_soc_ocv (cell_voltage)           # get intial SOC from the open circuit voltage curve
    thermal_coefficient = get_thermal_coefficient (temperature)
    if True: 
        state_of_charge = state_of_charge + current* time_two_readings*thermal_coefficient/ total_cell_capacity
        print(state_of_charge)
        time.sleep (5)                     # to wait 5 seconds between readings
    return state_of_charge
#************************************************************************#
def runall():
  run1()
  cell1_state_of_charge= soc(cell1_current,cell1_voltage,temperature)
  print(cell1_state_of_charge)

runall()