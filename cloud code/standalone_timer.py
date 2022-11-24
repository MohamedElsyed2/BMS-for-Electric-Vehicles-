
import time
def timer ():
    file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/timer.txt", "r")  
    timer_1 = int (file.read())
    file.close()
    if timer_1 >= 4294967295:               # to prevent the timer from overflow.
        timer_1 = 1
    else:
        timer_1 += 1
    file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/timer.txt", "w")
    file.truncate()       # delete the last value of number of cycles.
    file.write(str(timer_1))
    file.close()
    time.sleep(60)                    # wait for 60 seconds.


def run():
    while True:
        timer()

#run()