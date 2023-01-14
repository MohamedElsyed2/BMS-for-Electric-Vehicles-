import matplotlib.pyplot as plt
import numpy

def charging_voltage_charging_tim_plot():

    # charging_tim axis values
    SOC = [0.00,5.00,10.00,15.00,20.00,25.00,30.00,35.00,40.00,45.00,50.00,55.00,60.00,65.00,70.00,75.00,80.00,85.00,90.00,95.00,100.00]    # SOC axis values
    OCV = [3.44,3.47,3.52,3.55,3.58,3.6,3.61,3.63,3.64,3.67,3.68,3.72,3.75,3.8,3.84,3.88,3.94,3.99,4.04,4.11,4.18]  
    # charging_tim = [0.00 , 94.5]    # X-axis values
    # capacity_axis = [0.0, 2560 ] 
    global fig
    fig, curve = plt.subplots()
    curve.plot(SOC, OCV, color="blue", marker='o', markerfacecolor='red')
    curve.set(xlabel='State of Charge (SOC)', ylabel='Open Circuit Voltage (OCV) (V)',title='')
    
    curve.set_ylim(3.3 , 4.5)
    curve.set_xlim(-5.00 , 105.00)
    curve.grid(True)
    plt.show()
charging_voltage_charging_tim_plot()