import os

def creation_folder(Test):
    os.system("mkdir -p "+ Test)


def question(Device_Model, Test):

    print("---------------------Possible Modes---------------------\n")
    print("1) Locked")
    print("2) Idle")
    print("3) Active")
    print("4) Application running")
    print("5) BT inquiry")
    print("6) Save Battery mode")
    print("7) Save Battery mode, Display off")
    print("8) Sending Data")
    print("9) Receiving Data")
    print("10) Audio Sending File")
    print("\n")
    path=[]
    question = input("Which is the device mode? ")

    if question=="1":
        creation_folder(Test+"/"+Device_Model+"/Locked")
        path=Test+"/"+Device_Model+"/Locked"

    if question == "2":
        creation_folder(Test + "/" + Device_Model + "/Idle")
        path = Test + "/" + Device_Model + "/Idle"

    if question == "3":
        creation_folder(Test + "/" + Device_Model + "/Active")
        path = Test + "/" + Device_Model + "/Active"

    if question == "4":
        creation_folder(Test + "/" + Device_Model + "/Applicationa_running")
        path = Test + "/" + Device_Model + "/Applicationa_running"

    if question == "5":
        creation_folder(Test + "/" + Device_Model + "/BT_inquiry")
        path = Test + "/" + Device_Model + "/BT_inquiry"

    if question == "6":
        creation_folder(Test + "/" + Device_Model + "/Save_Battery")
        path = Test + "/" + Device_Model + "/Save_Battery"

    if question == "7":
        creation_folder(Test + "/" + Device_Model + "/Save_Battery_DisplayOFF")
        path = Test + "/" + Device_Model + "/Save_Battery_DisplayOFF"

    if question == "8":
        creation_folder(Test + "/" + Device_Model + "/SendingData")
        path = Test + "/" + Device_Model + "/SendingData"

    if question == "9":
        creation_folder(Test + "/" + Device_Model + "/ReceivingData")
        path = Test + "/" + Device_Model + "/ReceivingData"

    if question == "10":
        creation_folder(Test + "/" + Device_Model + "/AudioSending")
        path = Test + "/" + Device_Model + "/AudioSending"




    return path

def pathTest2(path, cycles):
    creation_folder(path+"/"+cycles)
    path=path+"/"+cycles
    print(path)
    return path






