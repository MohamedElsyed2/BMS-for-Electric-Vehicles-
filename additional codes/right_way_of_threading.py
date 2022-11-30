

#################################################################
# Python program to illustrate the concept
# of threading
# importing the threading module
import threading
import time
 
def func1():
    global a
    time.sleep(1)
    a = 4
 
def print_b():
    global b
    time.sleep(3)
    b= 5
 
def run():
    while True:
        # creating thread
        t1 = threading.Thread(target=print_b)
        t2 = threading.Thread(target=func1)
        start = time.time()
        t1.start()              # starting thread 1
        t2.start()               # starting thread 2
        t1.join()   # wait until thread 1 is completely executed
        t2.join()    # wait until thread 2 is completely executed
        end = time.time()
        # both threads completely executed
        print(b*a)
        print('Time taken in seconds -', end - start)
run()