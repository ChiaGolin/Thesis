import Folder as f
import Device
import datetime
import L2ping as L2
import os

date_time=str(datetime.datetime.now())
Test="Test1"
print("************************** TEST 1 ****************************\n")

#   Creation of folders
f.creation_folder(Test)

#  Device definition
bd_addr, bd_name=Device.lines()

#  Creation of subfolder with name of device and status
path=f.question(str(bd_name),Test)

# definition of i-th run (definition of file name)
c=input("choose path test: ")
if c=="1":
    k=1
    t=21
else:
    k=21
    t=41


#  L2 ping
for i in range (k,t):
    L2.standard(bd_addr, path, i)

