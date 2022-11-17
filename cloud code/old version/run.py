import client2
import module
import datetime
import threading


thread_6 = threading.Thread(target=client2.cycle_life)
thread_6.start()
thread_7 = threading.Thread(target=module.battery_age)
thread_7.start()
