import connect_subscribe_getMeasseges
import cycle_life_prediction
import threading


thread_1 = threading.Thread(target=connect_subscribe_getMeasseges.run)
thread_1.start()
thread_2 = threading.Thread(target=cycle_life_prediction.run)
thread_2.start()
