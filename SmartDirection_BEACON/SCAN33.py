#!/usr/bin/env python
from __future__ import print_function
import sys
import queue
import datetime
import xml.etree.ElementTree as ET
import keyboard
import time
import threading
import pprint as pp

# my import
import Publish as Pub
import blescan2 as ble
import xml_parser



FILTER_MODE = 0
TIME = 3600


class timer_Thread(threading.Thread):

    def __init__(self, sec, timer_queue, id, stop_timer):
        threading.Thread.__init__(self)
        self.sec = sec
        self.timer_queue = timer_queue
        self.id = id
        self.stop_timer = stop_timer

    def run(self):
        time.sleep(self.sec)
        if self.stop_timer.empty():
            self.timer_queue.put("stop")

        else:
            self.stop_timer.get()


def check_proximity(rssi):
    print(rssi)
    if rssi < (-75.24):
        status = "Really far away"

    if rssi < (-70.43) and rssi >= (-75.24):
        status = "Far away"

    if rssi < (-67.08) and rssi >= (-70.43):
        status = "Is coming"

    if rssi < (-60.41) and rssi >= (-67.08):
        status = "Close"

    if rssi >= (-60.41):
        status = "Really close"

    return status


def filter_mode(rssi, filter, alfa, rssi_past):
    # alfa*RSSI(t)+(1-alfa)*RSSI(t-1)

    temp2 = 0
    print("prima    " +str(filter))
    for i in range(0, len(filter) - 1):

        if i == 0:
            temp1 = filter[i]
            temp2 = filter[i + 1]
        else:
            temp1 = temp2
            temp2 = filter[i + 1]

        filter[i + 1] = temp1

    filter[0] = rssi

    # FILTER IMPLEMENTATION
    for i in range(1, len(filter)):
        rssi_past = float(rssi_past) + float((pow((1 - alfa), i)) * float(filter[i]))

    rssi = (float(filter[0]) * alfa + rssi_past)  
    filter[0]=rssi

    return rssi


def open_map(map_path):
    tree = ET.parse(map_path)
    root = tree.getroot()
    return root


class user(threading.Thread):
    def __init__(self, data, ble_list, direction_q, del_direction_q, delate_user, stop_queue, broker, topic_name,
                 rasp_id):
        threading.Thread.__init__(self)
        self.data = data
        self.ble_list = ble_list
        self.direction_q = direction_q
        self.del_direction_q = del_direction_q
        self.delate_user = delate_user
        self.stop_queue = stop_queue  
        self.broker = broker
        self.topic_name = topic_name
        self.rasp_id = rasp_id
        

    def run(self):

        ##################      INITIALIZATION        #####################

        ########################
        ##       QUEUE        ##
        ########################

        # TIMER QUEUES
        timer_queue = queue.Queue()
        stop_timer = queue.Queue()

        ########################
        ##       ARRAY        ##
        ########################

        # MAC LIST
        MAcList = []

        # RSSI LIST
        rssi_list = []

        ###########################
        ##       VARIABLE        ##
        ###########################

        # LOOP VARIABLE
        exit = 0

        # FOUND FLAG
        found = 0
        
        analisi=0

        # VARIABLES FOR FILTERING
        FILTER = 2
        filter = [0] * FILTER
        alfa = 0.80
        rssi_past = 0

        # THRESHOLD
        THRESHOLD = -70.43
        POS_THRESHOLD = THRESHOLD
        NEG_THRESHOLD = THRESHOLD

        # SCALING THRESHOLD VALUE
        delta = 2

        # NEAR FLAG
        near = 0

        # ARRIVED FLAG
        arrived = 0

        # ITERATION COUNT
        iteration = 0

        # FOR
        for_flag = 0

        # OUT OF RANGE
        out = 0

       

        #STATUS
        status="Null"

        tmp_dict = {}

        #NOT FOUND FLAG
        count=0
        
        ##################      START        #####################

        # CREATE A LIST OF JUST MAC
        for i in range(0, len(self.data["mac"])):
            MAcList.append(self.data["mac"][i])
        
        print(str(MAcList))
        # OPEN XML MAP
        
        root = open_map("map1.xml")
        
        # TIMER
        TIMER = timer_Thread(TIME, timer_queue, self.data["id"], stop_timer)
        TIMER.setDaemon(True)
        TIMER.start()
        p=datetime.datetime.now()
        # DIRECTION AND FINAL
        direction, final = xml_parser.find_direction(root, self.data["place_id"], self.rasp_id)
        
        
        # ALIVE USER LOOP
        while exit == 0:
            
            #   MQTT STOP
            if not self.stop_queue.empty():

                stop_id = self.stop_queue.get()
                print("MQTT STOP of " + stop_id + "\n")

                if stop_id == self.data["id"]:
                    # DELATE ARROW
                    self.del_direction_q.put(self.data['id'])

                    # EXIT LOOP
                    exit = 1


            if len(self.ble_list) > 0:
               
                tmp_dict = self.ble_list

               
                for i in range(0, len(MAcList)):
                    analisi=1
                    for key, val in tmp_dict.copy().items():
                        if key == MAcList[i]:
                            
                            for j in range(0, len(val['rssi'])):
                                rssi_list.append(float(val['rssi'][j]))
                                found = 1
                
                if analisi==1:
                    analisi=0
                    
                    if found == 0:
                        rssi_list = []
                        POS_THRESHOLD = THRESHOLD
                        NEG_THRESHOLD = THRESHOLD
                        
					
                        print("----------NOT FOUND---------------")
						# CHECK IF IT IS NOT FOUND FOR AT LEAST TWO TIMES IN A ROW
                        if count==1:
                            
                            if out == 1:
                                out = 0
                                self.del_direction_q.put(self.data["id"])
                                if near == 1:
                                    near = 0
                        else:
                            count=1




            # BEACON IN THE SYSTEM
                    if found == 1:
                        
                        found=0
                        count=0

                        # RSSI AVERAGE
                        rssi = float(ble.RSSI_ave(rssi_list))
                                            

                                          


                        # FILTER MODE

                        if FILTER_MODE == 1:
                            rssi =  float("{0:.2f}".format(filter_mode(rssi, filter, alfa, rssi_past)))
                            rssi_past = 0
                            print("----"+str(filter))



                        rssi_list = []

                        # PROXMITY STATUS
                        status = check_proximity(rssi)

                        print("Beacon " + str(self.data["id"]) + "\t" + str(rssi) + "\t" + str(status) + "\t" + str(
                            self.data["place_id"]) + "\t" + str(direction) + "\n")

                        # TIMER EXPIRE
                        if not timer_queue.empty():
                            print("TIMER EXPIRED\n")
                            timer_queue.get()

                            # DELATE ARROW
                            self.del_direction_q.put(self.data['id'])

                            # DELATE USER
                            self.delate_user.put(self.data['id'])

                            # EXIT LOOP
                            exit = 1

                        elif final == True and float(rssi) >= THRESHOLD and arrived == 1:

                            stop_timer.put("stop")

                            # STOP PUBLISH
                            Pub.publishing_stop(self.broker, self.topic_name[1], self.data["id"])
                            arrived=0

                            time.sleep(2)

                        else:

                            # PROJECTION DATA
                            return_dict = {"direction": direction,
                                           "color": self.data["color"],
                                           "id": self.data["id"],
                                           "mac": self.data["mac"],
                                           "timestamp": self.data["timestamp"],
                                           "beacon_flag": 1}

                            if rssi >= POS_THRESHOLD and near == 0:

                                # USER IN RANGE and NEAR
                                print("USER NOW IS NEAR\n")

                              
                                near = 1

                                # UPDATE THRESHOLD
                                NEG_THRESHOLD = POS_THRESHOLD - delta
                                iteration = 0
                                print("NEG: " + str(NEG_THRESHOLD))

                                # ADD ARROW
                                self.direction_q.put(return_dict)
                                count_p = 0
                                out = 1

                                # USER IS JUST ARRIVED
                                if final == True:
                                    arrived = 1
                                    time.sleep(25)

                            


                            elif rssi < (NEG_THRESHOLD) and near == 1:
                                
                                near = 0
                                

                                # USER IN RANGE, but FAR AWAY
                                print("USER NOW IS FARAWAY AGAIN\n")



                                # UPDATE THRESHOLD
                                POS_THRESHOLD = NEG_THRESHOLD + delta
                                iteration = 0
                                print("POS: " + str(POS_THRESHOLD))

                                if out == 1:
                                    out = 0

                                    # DELATE ARROW
                                    self.del_direction_q.put(return_dict["id"])

                                

            time.sleep(0.5)

    
            rssi_list = []
            

        sys.exit()