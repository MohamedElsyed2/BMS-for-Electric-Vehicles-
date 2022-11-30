

#################################################################
# Python program to illustrate the concept
# of threading
# importing the threading module
import threading
import time
 
def func1(num):
    global a
    time.sleep(1)
    a = 5
    number = str(num)
    try:
        file = open("E:\Masterarbeit\BMS-for-Electric-Vehicles-/additional codes/test"+number+".txt", "w")
        file.truncate()      
        file.write(str(a))
    finally:
        file.close()
 
# def print_b(num):
#     global b
#     time.sleep(3)
#     b= num
 
def run():
    while True:
        # creating thread
        t1 = threading.Thread(target=func1, args=(1,))
        t2 = threading.Thread(target=func1, args=(2,))
        start = time.time()
        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
    
        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()
        end = time.time()
        # both threads completely executed
        # print(b*a)
        print('Time taken in seconds -', end - start)
run()