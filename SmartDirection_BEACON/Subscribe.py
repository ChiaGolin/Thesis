#!/usr/bin/env python
import paho.mqtt.client as mqtt
import sys
import json
import ast
import threading


def on_connect(self, client, obj, flags, rc):
    print("connection result: " + str(rc))

def json_file(dict):

    json_file=dict["id"] + '.json'
    with open(json_file, 'w') as f:
        json.dump(dict, f)

    return json_file

class Receive_on_message:

    def __init__(self, queue_sub, del_queue):
        self.queue_sub = queue_sub
        self.del_queue=del_queue





    def on_message(self, client,userdata, msg):

        Msg = str(msg.payload.decode("utf-8"))

        # SUBSCRIPTION TOPIC: START
        if msg.topic == "topic/rasp4/directions/start":
            print("START TOPIC: "+ msg.topic)
            #print("RECEIVED MESSAGE: " + Msg+"\n")

            # CREATION OF JSON FILE
            #{
            #   "id": "",
            #   "mac": "",
            #   "place_id": "",
            #   "timestamp": "",
            #   "color": "",
            #   "beacon_flag": ""
            #   }

            json_name=json_file(ast.literal_eval(Msg))

            if len(msg.payload)>0:

                # SENDING OF JSON FILE
                self.queue_sub.put(json_name)

        # SUBSCRIPTION TOPIC: STOP
        elif msg.topic == "topic/rasp4/directions/stop":
            print("STOP TOPIC: "+msg.topic)
            print("RECEIVED MESSAGE: " + Msg)
            self.del_queue.put(str(msg.payload.decode("utf-8")))






def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid))
    pass

def on_log(client, obj, level, string):
    print(string)

def print_msg(client, userdata, message):
    print("%s : %s" % (message.topic, message.payload))

class subscribing_thread(threading.Thread):
    def __init__(self, broker,topic_name, queue, del_queue):
        threading.Thread.__init__(self)
        self.broker = broker
        self.topic_name1=topic_name
        self.client = mqtt.Client()
        self.queue = queue
        self.del_queue = del_queue


    def run(self):

        receiver =  Receive_on_message(self.queue, self.del_queue)
        self.client.on_message= receiver.on_message


        print("CONNECTING TO  ", self.broker)
        try:
            self.client.connect(self.broker)

        except:
            print("CANNOT CONNECT")
            sys.exit(1)


        self.client.subscribe(self.topic_name1[0], qos=1)
        self.client.subscribe(self.topic_name1[1], qos=1)



        print("SUBSCRIBED on TOPICS:\n" + self.topic_name1[0] + " QoS: 1\n" + self.topic_name1[1] + " QoS: 1\n")

        self.client.loop_forever()







