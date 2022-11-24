import connect_subscribe_getMeasseges
import cycle_life_prediction
import state_of_health
import state_of_charge
import standalone_timer
import threading


thread_1 = threading.Thread(target=connect_subscribe_getMeasseges.run)
thread_1.start()
thread_2 = threading.Thread(target=cycle_life_prediction.run)
thread_2.start()
thread_3 = threading.Thread(target=state_of_health.run)
thread_3.start()
thread_4 = threading.Thread(target=state_of_charge.run)
thread_4.start()
thread_5 = threading.Thread(target=standalone_timer.run)
thread_5.start()