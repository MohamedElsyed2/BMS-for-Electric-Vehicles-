

import connect_subscribe_getMeasseges
import run_cycle_life_prediction
import state_of_health
import state_of_charge
import standalone_timer
import update_coulombic_efficincy
import check_battery_usage 
import number_of_cycles_counter
import threading

# thread_1 = threading.Thread(target=connect_subscribe_getMeasseges.run)
# thread_1.start()
# #thread_1.join() # # wait until thread 1 is completely executed; until connect to the broker, subscribe to the required topics, and get measseges and sensors reagings.
thread_2 = threading.Thread(target=run_cycle_life_prediction.run)
thread_2.start()
# thread_3 = threading.Thread(target=state_of_health.run)
# thread_3.start()
# thread_6 = threading.Thread(target=update_coulombic_efficincy.run)
# thread_6.start()
# thread_4 = threading.Thread(target=state_of_charge.run)
# thread_4.start()
# thread_5 = threading.Thread(target=standalone_timer.run)
# thread_5.start()
thread_7 = threading.Thread(target=check_battery_usage.run)
thread_7.start()
# thread_8 = threading.Thread(target=number_of_cycles_counter.run)
# thread_8.start()
while True:
    connect_subscribe_getMeasseges.run()
    state_of_health.run()
    state_of_charge.run()
    standalone_timer.run()
    update_coulombic_efficincy.run()