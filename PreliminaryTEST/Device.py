def lines():
    bd_addr = []
    bd_name = []
    f=open("MAC_Devices.txt", "r")
    f1 = open("MAC_Devices.txt", "r")
    print(f.read())
    print("\n")
    chosen_line = input("Choose MAC address of the bluetooth device: ")

    for lin in f1:

        if lin[0] == chosen_line:
            bd_addr = lin[2:19]
            bd_name = lin[20:-1]
            print(bd_addr, bd_name)

    f.close()
    return bd_addr, bd_name




