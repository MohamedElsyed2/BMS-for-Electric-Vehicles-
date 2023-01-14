import matplotlib.pyplot as plt
import numpy

def charging_voltage_charging_tim_plot():

    # charging_tim axis values
    charging_tim = [94.5 , 104 , 116.5, 135 , 175]       # X-axis values
    charging_voltage = [2560 , 2750, 2880 , 2980, 3080]      # Y-axis values
    # charging_tim = [0.00 , 94.5]    # X-axis values
    # capacity_axis = [0.0, 2560 ] 
    global fig
    fig, curve = plt.subplots()
    curve.plot(charging_tim, charging_voltage, color="blue", marker='o', markerfacecolor='red')
    curve.set(xlabel='charging_tim %', ylabel='charging_voltage (V)',title='The relation between charging_voltage and charging_tim')
    # ymin = 2.4
    # xmin = 0

    # time12= 30
    # #charging_timIntial= numpy.exp(numpy.interp([voltage], y[::-1], numpy.log(x[::-1])))
    # charging_volt =float("{:.4f}".format(numpy.interp(time12, charging_tim[::1], charging_voltage[::1])))
    # print(charging_volt)
    # voltage= 3.925
    # #charging_timIntial= numpy.exp(numpy.interp([voltage], y[::-1], numpy.log(x[::-1])))
    # charging_timIntial =float("{:.2f}".format(numpy.interp(voltage, charging_tim[::1], charging_voltage[::1])))
    # print(charging_timIntial)
    # for xi, yi in [(charging_timIntial, y1), (x2, y2)]:
    #     ax.hlines(yi, xmin, xi, color='r')
    #     ax.vlines(xi, ymin, yi, color='r')
    #     print(f'x-value corresponding to y={10}: {xi:.3f}')
    curve.set_ylim(2000 , 3500)
    curve.set_xlim(90 , 180)
    #curve.set_xscale('log')
    curve.grid(True)
    plt.show()
charging_voltage_charging_tim_plot()