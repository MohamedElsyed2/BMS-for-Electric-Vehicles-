
import threading
import time
import cycle_life_prediction

def run():
    thread_1 = threading.Thread(target=cycle_life_prediction.run, args=(1,))
    thread_2 = threading.Thread(target=cycle_life_prediction.run, args=(2,))
    thread_3 = threading.Thread(target=cycle_life_prediction.run, args=(3,))
    
    thread_1.start()
    time.sleep(5)
    thread_2.start()
    time.sleep(5)
    thread_3.start()
    time.sleep(5)
    

run()
