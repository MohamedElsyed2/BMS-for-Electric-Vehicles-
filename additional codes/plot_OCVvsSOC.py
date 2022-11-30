import matplotlib.pyplot as plt
import numpy

def OCV_SOC_plot():

    # SOC axis values
    SOC = [0.00,0.00,0.00,5.00,10.00,15.00,20.00,25.00,30.00,35.00,40.00,45.00,50.00,55.00,60.00,65.00,70.00,75.00,80.00,85.00,90.00,95.00,100.00]
    # corresponding OCV axis values
    OCV = [2.4,2.5,2.6,2.8,2.99,3.15,3.21,3.28,3.29,3.3,3.31,3.32,3.35,3.37,3.39,3.4,3.45,3.5,3.55,3.56,3.6,3.61,3.62]
    global fig
    fig, curve = plt.subplots()
    curve.plot(SOC, OCV, color="blue", marker='o', markerfacecolor='red')
    curve.set(xlabel='SOC %', ylabel='OCV (V)',title='The relation between OCV and SOC')
    ymin = 2.4
    xmin = -5.0

    voltage= 3.57
    #socIntial= numpy.exp(numpy.interp([voltage], y[::-1], numpy.log(x[::-1])))
    socIntial =float("{:.2f}".format(numpy.interp(voltage, OCV[::1], SOC[::1])))
    print(socIntial)
    # for xi, yi in [(socIntial, y1), (x2, y2)]:
    #     ax.hlines(yi, xmin, xi, color='r')
    #     ax.vlines(xi, ymin, yi, color='r')
    #     print(f'x-value corresponding to y={10}: {xi:.3f}')
    curve.set_ylim(ymin, 3.8)
    curve.set_xlim(xmin, 100.00)
    #curve.set_xscale('log')
    curve.grid(True)
    plt.show()
OCV_SOC_plot()