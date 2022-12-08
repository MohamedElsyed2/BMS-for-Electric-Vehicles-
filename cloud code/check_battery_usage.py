
import time

def check_battery_being_used_or_not ():
    timer = 0
    while timer <= 72:          # 72       # check battery usage every 72 hour= 3 days.
        try:
            file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/module1_current.txt", "r")   # open the file 'temperature.txt' in raeding mode.
            battery_current = float (file.read())
        finally:
            file.close()
      
        if battery_current != 0:            # like a watchdog, if battery current is not equal to zero, then the battery is in service.
            try:
                file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/check_battery_being_used.txt", "w")   # open the file 'temperature.txt' in raeding mode.
                file.truncate()       
                file.write("1")
            finally:
                file.close()
            timer = 0                  # to restart the timer.
        elif battery_current == 0:     # if the battery current still equals to zero then increment the timer and go to the next iteration.
            time.sleep(3600)                 # 3600 second = 1 hour.
            timer += 1 
    try:
        file = open("E:/Masterarbeit/BMS-for-Electric-Vehicles-/cloud code/check_battery_being_used.txt", "w")   # open the file 'temperature.txt' in raeding mode.
        file.truncate()       
        file.write("0")
    finally:
        file.close()
 
def run():
    while True:
        check_battery_being_used_or_not()

#run()