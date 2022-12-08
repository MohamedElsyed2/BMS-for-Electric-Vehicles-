
from math import exp

a = 0.0039
b = 1.95
c = 67.51
d = 2070
temperature = 25
nominal_temperature = 25
num_cycle_life_temp = (a*pow(temperature,3) - b*pow(temperature,2) + c*temperature + d)/(a*pow(nominal_temperature,3) - b*pow(nominal_temperature,2) + c*nominal_temperature + d)

disch_current = 0
nominal_disch_current = 1                       # from datasheet
e = 4464
f = -0.1382
g = -1519
h = -0.4305
num_cycle_life_disch_current = (e*exp(f*disch_current)+g*exp(h*disch_current))/(e*exp(f*nominal_disch_current)+g*exp(h*nominal_disch_current))


charging_current = 0
nominal_charging_current = 0.7
m = 5963
n = -0.6531
o = 321.4
p = 0.03168
num_cycle_life_charging_current = (m*exp(n*charging_current)+o*exp(p*charging_current))/(m*exp(n*nominal_charging_current)+o*exp(p*nominal_charging_current))

q = 1471
u = 0.3369
v = -2.295
s = 214.3
t = 0.6111
dod = 0
average_SOC = 50
nominal_dod = 100
nominal_average_SOC = 50
real_cycle_life = q+((u/(2*v))*(s+100*u)-200*t)*dod + s*average_SOC + t* pow(dod,2) + u*dod*average_SOC + v* pow(average_SOC,2)
nominal_cycle_life = q+((u/(2*v))*(s+100*u)-200*t)*nominal_dod + s*nominal_average_SOC + t* pow(nominal_dod,2) + u*nominal_dod*nominal_average_SOC + v* pow(nominal_average_SOC,2)
num_cycle_life_SOC_DOD = real_cycle_life / nominal_cycle_life


nominal_cycle_life = 649                                        # from battery datasheet.
equivelant_battery_num_cycle_life = int (nominal_cycle_life * num_cycle_life_temp * num_cycle_life_disch_current * num_cycle_life_charging_current * num_cycle_life_SOC_DOD)
print(equivelant_battery_num_cycle_life)