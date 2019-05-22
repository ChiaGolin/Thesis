#!/usr/bin/env python
import Publish as Pub

s=input("choose beacon: ")


if s=="A":
    dict = {"id": "A","mac":  ["e9:77:df:b8:f9:8c","ea:78:e0:b9:fa:8d", "eb:79:e1:ba:fb:8e", "ec:7a:e2:bb:fc:8f", "ed:7b:e3:bc:fd:90"],"place_id": "3403", "timestamp": "165919 061018", "color": "red", "beacon_flag": "1"}

elif s=="B":
    dict={"id": "B", "mac": [ "e3:f0:2a:8e:f0:3a", "e4:f1:2b:8f:f1:3b", "e5:f2:2c:90:f2:3c", "e7:f4:2e:92:f4:3e", "f7:0b:59:ce:94:4bs"], "place_id": "0001", "timestamp": "150921 271018", "color": "red", "beacon_flag": "1"}
elif s=="C":
    dict={"id": "C","mac": ["ef:66:9a:a6:31:e7","f9:a1:e5:95:00:fc", "fa:a2:e6:96:01:fd", "fb:a3:e7:97:02:fe", "fd:a5:e9:99:04:00"],"place_id": "0004", "timestamp": "135900 171018", "color": "yellow", "beacon_flag": "1"}

elif s=="1":
    dict={"id": "123","mac": "38:A4:ed:2a:1b:5b","place_id": "0004", "timestamp": "135900 171018", "color": "yellow", "beacon_flag": "0"}

elif s=="2":
    dict = {"id": "123", "mac": "38:A4:ed:2a:1b:5b", "place_id": "0001", "timestamp": "135900 171018","color": "yellow", "beacon_flag": "0"}

elif s=="3":
    dict = {"id": "123", "mac": "1C:66:AA:CC:9A:18", "place_id": "0001", "timestamp": "135900 171018",
            "color": "yellow", "beacon_flag": "0"}

json_file=str(dict)
broker="10.79.1.112"
#broker="10.79.5.210"
#broker="127.0.0.1"
#broker="10.79.1.176"
topic_name =["topic/rasp4/directions/start", "topic/rasp4/directions/stop"]


Pub.publishing_start(json_file, broker, topic_name[0])

#{"id": "B", "mac": ["e3:f0:2a:8e:f0:3a", "e4:f1:2b:8f:f1:3b", "e5:f2:2c:90:f2:3c", "e6:f3:2d:91:f3:3d", "e7:f4:2e:92:f4:3e", "ec:c8:6a:90:86:10"], "place_id": "0001", "timestamp": "150921 271018", "color": "blue", "beacon_flag": 1}

#{"id": "A", "mac": ["ea:78:e0:b9:fa:8d", "eb:79:e1:ba:fb:8e", "ec:7a:e2:bb:fc:8f", "ec:90:fb:c4:31:f8", "ed:7b:e3:bc:fd:90"], "place_id": "3403", "timestamp": "165919 061018", "color": "red", "beacon_flag": "1"}

#{"id": "C", "mac": ["ec:f2:03:e2:6a:c4", "fa:a2:e6:96:01:fd", "fb:a3:e7:97:02:fe", "fc:a4:e8:98:03:ff", "fd:a5:e9:99:04:00"], "place_id": "0004", "timestamp": "135900 171018", "color": "yellow", "beacon_flag": 1}
    