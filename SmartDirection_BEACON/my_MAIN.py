#!/usr/bin/env python
import threading
import time
import json
import logging
import os
from collections import namedtuple
import sys

import queue
import datetime
from time import strftime, localtime

#my imports

import Subscribe as Sub
import SCAN33 as SCAN1
import blescan2 as ble
import DISPLAY


#   BROKER ADDRESS
local_host="127.0.0.1"
polimi_server="10.79.1.112"
amazon_server="18.191.127.255"


#   MQTT SETTING
topic_name =["topic/rasp4/directions/start", "topic/rasp4/directions/stop"]
broker=amazon_server

#raspberry setting
rasp_id ="C"

#queue dimention
BUF_SIZE = 10


global beacon_list
beacon_list=[]

global stop_Beaconlist
stop_Beaconlist = []


global display_Ready

class Thread_Thread(threading.Thread):
    def __init__(self, arrow_display, wait, display_Ready_q):
        threading.Thread.__init__(self)
        self.arrow_display = arrow_display
        self.wait = wait
        self.display_Ready_q = display_Ready_q

    def run(self):



        ############# DISPLAY THREAD #####################
        DISP = DISPLAY.DisplayArrow(self.arrow_display, self.wait, self.display_Ready_q)
        print("LOADING DISPLAY...\n")
        DISP.Go()

class arrow_Thread(threading.Thread):
    def __init__(self, direction_q, del_direction_q, display_Ready_q):
        threading.Thread.__init__(self)
        self.direction_q= direction_q
        self.del_direction_q = del_direction_q
        self.display_Ready_q = display_Ready_q

    def run(self):

        # SYNCHRONIZATION QUEUE
        arrow_display = queue.Queue(1)
        wait = queue.Queue(1)

        # UPDATE LIST OF ARROW
        list_arrow = []

        # LIST ID/MAC
        identifier_list=[]

        #Del ok
        del_ok=0

        ####### DISPLAY THREAD #########
        THREAD_THREAD = Thread_Thread(arrow_display, wait, self.display_Ready_q)
        THREAD_THREAD.setDaemon(True)
        THREAD_THREAD.start()

        # INFINTE LOOP
        while True:

            # READ NEW ARROW
            while not self.direction_q.empty():

                print("########## NEW ARROW ARRIVAL ###########\n")
                prov_add = self.direction_q.get()

                # LIST OF USER IN THE SYSTEM

                identifier_list.append(prov_add["id"])

                # LIST WITH ALL REQUIRED PROJ DATA
                list_arrow.append(prov_add)




            while not self.del_direction_q.empty():

                print("########## DELATING ARROW ############\n")
                prov_del = self.del_direction_q.get()

                print(prov_del)
                print(str(identifier_list))
                if prov_del in identifier_list:
                    print("-----------------------------"+str(prov_del))
                    for i in range(0, len(list_arrow)):
                        # SEARCHING IN THE LIST ARROW OF THE ARROW THAT HAVE TO BE DELATED
                        print(str(list_arrow[i]["id"])+"---"+str(prov_del))
                        if list_arrow[i]["id"] == prov_del:
                            idx = i
                            print(idx)
                            del_ok=1
                            break
                    if del_ok==1:    
                        del list_arrow[idx]
                        del identifier_list[idx]
                        del_ok=0

            
            if len(list_arrow) > 0:
                for i in range(0, len(list_arrow)):
                    arrow_display.put(list_arrow[i])
                    wait.get()



def stop_beacon(id_del):

    global stop_Beaconlist

    for i in range(0, len(stop_Beaconlist)):

        if id_del==stop_Beaconlist[i][1]:
            stop_Beaconlist[i][0].put(id_del)




if __name__ == "__main__":

    ##################      INITIALIZATION        #####################
    os.system('sudo hciconfig hci0 down && sudo hciconfig hci0 up')
    ########################
    ##       QUEUE        ##
    ########################

    # PROJECTION QUEUE
    direction_q = queue.Queue(BUF_SIZE)
    del_direction_q = queue.Queue(BUF_SIZE)

    # MQTT QUEUE
    sub_q = queue.Queue(1)  # SUBSCRIPTION
    del_q = queue.Queue(BUF_SIZE)  # STOP PUBLISH

    # DELATING USER QUEU
    delate_Beacon_user = queue.Queue(BUF_SIZE)  # [BEACON]


    #DISPLAY READY
    display_Ready_q = queue.Queue(1)

    #BLE SCAN
    ble_list_send = queue.Queue(BUF_SIZE)  # coda che aggiorna sulla scan la lista dei MAC




    ########################
    ##       ARRAY        ##
    ########################

    # LIST OF USERS PRESENT IN THE SYSTEM
    id_list = []        # [BEACON]


    #   ARRAY OF 10 DIFFERENT QUEUE
    stop_beacon_qList=[]     #  [BEACON]


    ###########################
    ##       VARIABLE        ##
    ###########################

    # NUMBER OF USERS IN THE SYSTEM
    number_of_user_BEACON = 0   #  [BEACON]


    # NEW USER FLAG
    new_user_BEACON = 0     # [BEACON]

    #OK DEL
    ok_del=0
    ok_del_t=0




    ##################      START        #####################

    #  CREATION LIST OF STOP_QUEUE

    #   [BEACON]
    for i in range(0, BUF_SIZE):
        stop_beacon_qList.append(queue.Queue())




    # ARROW THREAD [DISPLAY OPENING]
    ARROW = arrow_Thread(direction_q, del_direction_q, display_Ready_q)
    ARROW.setDaemon(True)
    ARROW.start()

    while display_Ready_q.empty():
        time.sleep(1)

    # MQTT SUBSCRIPTION
    t_mqtt = Sub.subscribing_thread(broker, topic_name, sub_q, del_q)
    t_mqtt.setDaemon(True)
    t_mqtt.start()

    while True:

        # NEW USER ARRIVAL
        if not sub_q.empty():
            
            threads = sub_q.get()

            with open(threads) as f:
                try:
                    json_file = json.load(f)
                except:
                    print("Malformed json\n")



                # BEACON USER ARRIVAL

                if json_file["id"] not in beacon_list:
					
					# ADDITION TO BEACON LIST
                    beacon_list.append((json_file["id"]))
                    

					# UPDATE NUMBER USER IN THE SYSTEM
                    number_of_user_BEACON = number_of_user_BEACON + 1
					
					# NEW USER
                    new_user_BEACON = 1
                    
                    




        # ARRIVAL OF DELATE COMMAND FOR A DEVICE (MQTT STOP SENT FROM ANOTHER DESTINATION RASP)
        if not del_q.empty():
            del_msg = del_q.get()

            # DEL MESSAGE: BEACON ID
            if del_msg in beacon_list:

                # DECREASING OF BEACON USER IN THE SYSTEM
                number_of_user_BEACON=number_of_user_BEACON-1
                
                id_del = del_msg
				
				#DEL USER THREAD THROUGH QUEUE RESERVERVED FOR HIM
                stop_beacon(id_del)

				#UPDATE BEACON LIST
                for i in range(0, len(beacon_list)):
                    if beacon_list[i] == id_del:
                        ID_DEL = i
                        ok_del=1

                if ok_del==1:
                    del beacon_list[ID_DEL]
                    del stop_Beaconlist[ID_DEL]
                    ok_del=0


                # 10 QUEUES
                stop_beacon_qList.append(queue.Queue())


        # THERE ARE BEACON USER IN THE SYSTEM
        if  number_of_user_BEACON > 0:

            p=datetime.datetime.now()

            if len(beacon_list)>0:
                
                ble_list = ble.ScanScan()


                # NEW USER
                if new_user_BEACON==1:
                    

                    
                    #STOP BEACON LIST
                    stop_Beaconlist.append([stop_beacon_qList[number_of_user_BEACON-1],json_file["id"]])
                    

                    NEW_USER_BEACON = SCAN1.user(json_file, ble_list, direction_q, del_direction_q, delate_Beacon_user, stop_Beaconlist[len(stop_Beaconlist)-1][0], broker, topic_name, rasp_id)
                    NEW_USER_BEACON.setDaemon(True)
                    NEW_USER_BEACON.start()

                    new_user_BEACON=0


            if not delate_Beacon_user.empty():

                number_of_user_BEACON = number_of_user_BEACON - 1  # DECREASING ACTIVE USER
                
                id = delate_Beacon_user.get()

                #TIMER EXPIRED
                if id in beacon_list:

                    for i in range(0, len(beacon_list)):
                        if beacon_list[i] == id:
                            idx = i
                            ok_del_t=1
                    if ok_del_t==1:
                        del beacon_list[idx]
                        del stop_Beaconlist[idx]
                        ok_del_t=0
                












