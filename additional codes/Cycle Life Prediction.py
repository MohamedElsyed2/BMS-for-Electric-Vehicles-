from math import exp
import threading
import time
import array
import datetime
def get_measurements_compute():
    global temperature
    temperature = 25
    #************************* Start of battery_age_estimation method*****************************************#
    """ This method is coded according to the published paper: Muenzel, V.; de Hoog, J.; Brazil, M.; Vishwanath, A.; Kalyanaraman,
    S. A multi-factor battery cycle life prediction methodology for optimal battery management. 
    """
    def battery_age_estimation ():
        #******************* Start of battery_age_temperature method***********************************#
        def battery_age_temperature():
            global temperature                   # the real temperature of the battery cell.
            clT_array = array.array('f', [])   # clT_array: is the array of cycle life of temperature, 'f': stands for float.
            for i in range (0,4):
                a = 0.0039
                b = 1.95
                c = 67.51
                d = 2070
                nominal_temperature = 25
                num_cycle_life_temp = (a*pow(temperature,3) - b*pow(temperature,2) + c*temperature + d)/(a*pow(nominal_temperature,3) - b*pow(nominal_temperature,2) + c*nominal_temperature + d)
                clT_array.append (num_cycle_life_temp)  # adding an num_cycle_life_temp to the array.
                time.sleep(1)                    # time.sleep(21600)     # wait for 6 hours to get another value of num_cycle_life_temp.
            avr_num_cycle_life_temp= (clT_array[0]+clT_array[1]+clT_array[2]+clT_array[3])/4
            return avr_num_cycle_life_temp
        #******************* End of battery_age_temperature method***********************************#
        #********************************************************************************************#
        def get_chg_dischg_current():
            timer = 0
            global current_status_flag
            current_status_flag = False
            global total_incresed_SOC
            total_incresed_SOC = 0
            global total_decresed_SOC
            total_decresed_SOC = 0
            global total_chg_time
            total_chg_time = 0
            global total_dischg_time
            total_dischg_time = 0

            while timer < 86400:
                global before_SOC
                before_SOC = cell1_state_of_charge
                if current_status_flag == False:
                    time.sleep(60)
                    if cell1_current < 0:
                        current_status_flag = True
                    increased_SOC = cell1_state_of_charge - before_SOC
                    total_incresed_SOC = total_incresed_SOC + increased_SOC
                    total_chg_time = total_chg_time + 60                            # in secondes
                else:
                    time.sleep(60)
                    if cell1_current > 0:
                        current_status_flag = False
                        #stop_time = datetime.datetime.now()
                    decresed_SOC = before_SOC - cell1_state_of_charge 
                    total_decresed_SOC = total_decresed_SOC + decresed_SOC
                    total_dischg_time = total_dischg_time + 60
                timer = timer + 60
            global disch_current
            disch_current = ((total_decresed_SOC*2350)/(total_dischg_time/(3600)))/2350      # in coulomb
            global charging_current
            charging_current = ((total_incresed_SOC*2350)/(total_chg_time/(3600)))/2350

            #time.sleep(2)                           #time.sleep(86400)
        #********************************************************************************************#
        #******************* Start of battery_age_disch_current method*******************************#
        def battery_age_disch_current():
            #disch_current = get_chg_dischg_current()
            nominal_disch_current = 1                       # from datasheet
            e = 4464
            f = -0.1382
            g = -1519
            h = -0.4305
            num_cycle_life_disch_current = (e*exp(f*disch_current)+g*exp(h*disch_current))/(e*exp(f*nominal_disch_current)+g*exp(h*nominal_disch_current))
            return num_cycle_life_disch_current
        #******************* End of battery_age_disch_current method*******************************#
        #******************* Start of battery_age_charging_current method*******************************#
        def battery_age_charging_current():
            #charging_current = get_chg_dischg_current()
            nominal_charging_current = 0.7
            m = 5963
            n = -0.6531
            o = 321.4
            p = 0.03168
            num_cycle_life_charging_current = (m*exp(n*charging_current)+o*exp(p*charging_current))/(m*exp(n*nominal_charging_current)+o*exp(p*nominal_charging_current))
            return num_cycle_life_charging_current
        #******************* End of battery_age_charging_current method*******************************#
        #******************* Start of battery_age_SOC_DOD method*******************************#
        def battery_age_SOC_DOD():
            q = 1471
            u = 0.3369
            v = -2.295
            s = 214.3
            t = 0.6111
            dod = 60                                   # depth of discharge.
            average_SOC = 70
            nominal_dod = 100
            nominal_average_SOC = 50
            real_cycle_life = q+((u/(2*v))*(s+100*u)-200*t)*dod + s*average_SOC + t* pow(dod,2) + u*dod*average_SOC + v* pow(average_SOC,2)
            nominal_cycle_life = q+((u/(2*v))*(s+100*u)-200*t)*nominal_dod + s*nominal_average_SOC + t* pow(nominal_dod,2) + u*nominal_dod*nominal_average_SOC + v* pow(nominal_average_SOC,2)
            num_cycle_life_SOC_DOD = real_cycle_life / nominal_cycle_life
            return num_cycle_life_SOC_DOD
        #******************* End of battery_age_SOC_DOD method*******************************#
        nominal_cycle_life = 649
        thread_1 = threading.Thread(target=battery_age_temperature)
        thread_1.start()
        thread_2 = threading.Thread(target=get_chg_dischg_current)
        thread_2.start()
        equivelant_battery_num_cycle_life = int (nominal_cycle_life * battery_age_temperature() * battery_age_disch_current() * battery_age_charging_current() * battery_age_SOC_DOD())
        return equivelant_battery_num_cycle_life
    #************************* End of battery_age_estimation method*****************************************#
    #     equivelant_battery_num_cycle_life = battery_age_temperature() * battery_age_disch_current()
    #     return equivelant_battery_num_cycle_life
    # #************************* End of battery_age_estimation method*****************************************#
    
    print (battery_age_estimation ()) 

get_measurements_compute()
        