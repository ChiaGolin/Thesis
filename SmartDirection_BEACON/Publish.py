#!/usr/bin/python3

import logging
import paho.mqtt.client as mqtt

from collections import namedtuple
from  subprocess import call


def publishing_start(json_file, broker, topic_name):
    print("broker " + broker)
    print(json_file)
    call(["mosquitto_pub", "-h", broker, "-t", topic_name, "-m", json_file ])



def publishing_stop(broker, topic_name, message):
    print("STOP PUBLISH: "+topic_name)
    print("BROKER"+broker)
    call(["mosquitto_pub", "-h", broker, "-t", topic_name, "-m", message ])




