import threading
import Folder as f
import Device
import os
import mathmath as math
import L2ping as L2




Test="Test2"
print("************************** TEST 2 ****************************\n")

#   Creation of folders

f.creation_folder(Test)
bd_addr, bd_name=Device.lines()
c=input("choose part test: )")
if c=="1":
    k=1
    s=5
else:
    k=6
    s=11




path=f.question(str(bd_name),Test)



cycles=input("Enter number of multiple l2ping: ")
path=f.pathTest2(path, cycles)


ARRAY=[]



#creation of a new file, call function L2.readingPing that return max/min/ave values, writing on a file the average value
with open(path+"/Mean_"+c+".txt", 'a') as f:

    for p in range(k,s):

        namefile = str(1) + "_" + str(p)

        if os.path.getsize(path + "/" + namefile + ".txt") <= 0:


        if os.path.getsize(path+"/"+namefile+".txt") > 0:



            max_value, min_value, average_value=L2.readingPing(path, namefile)
            ARRAY.append(float(average_value))


    max_value, min_value, average_val=math.max_min_average(ARRAY)

    f.write(str(average_val))



