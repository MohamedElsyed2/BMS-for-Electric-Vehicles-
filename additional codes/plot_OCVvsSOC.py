import numpy as np
from matplotlib import pyplot as plt

def OCV_vs_SOC ():  
    # x axis values
    x = [1,2,3]
    # corresponding y axis values
    y = [2,4,1]
    
    # plotting the points 
    curve = plt.plot(x, y)
    
    # naming the x axis
    plt.xlabel('x - axis')
    # naming the y axis
    plt.ylabel('y - axis')
    
    # giving a title to my graph
    plt.title('My first graph!')
    plt.grid(True)

    # function to show the plot
    plt.show()
    #xdata = curve.get_xdata()
    ydata = curve.get_ydata()
    #print("X data points for the plot is: ", xdata)
    print("Y data points for the plot is: ", ydata)
    
    # plt.rcParams["figure.figsize"] = [7.50, 3.50]
    # plt.rcParams["figure.autolayout"] = True
    # y = np.array([1, 3, 2, 5, 2, 3, 1])
    # curve, = plt.plot(y, c='red', lw=5)
    # print("Extracting data from plot....")
    # xdata = curve.get_xdata()
    # ydata = curve.get_ydata()
    # print("X data points for the plot is: ", xdata)
    # print("Y data points for the plot is: ", ydata)
    # plt.show()
OCV_vs_SOC()