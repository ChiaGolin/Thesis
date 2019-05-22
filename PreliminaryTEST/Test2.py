import threading
import Folder as f
import Device
import datetime
import L2ping as L2
import ErrorCounter as err
import os

Test="Test2"
print("************************** TEST 2 ****************************\n")

#   Creation of folders

f.creation_folder(Test)
bd_addr, bd_name=Device.lines()
c=input("choose part test: )")
if c=="1":
    k=1
    l=6
else:
    k=6
    l=11



path=f.question(str(bd_name),Test)


cycles=input("Enter number of multiple l2ping: ")


pathx=path


path1=pathx+"/"+cycles
os.system("mkdir -p " + path1)

threads=[]



# multiple thread l2ping flood
for p in range (k,l):
    start_time = datetime.datetime.now()

    for i in range(1,int(cycles)+1):
        #creation of tread
        t = threading.Thread(target=L2.flood, args=(bd_addr, path1, i,str(p)))
        threads.append(t)
        t.start()

    for i in range(1, int(cycles)+1):
        #concatenation until the end
        t.join()


    # computation of running period

    end_time = datetime.datetime.now()
    delta_time = (end_time) - (start_time)

    h, m, s = str(delta_time).split(':')
    s0,s1=str(s).split(".")
    s=s0+s1

    s2 = "."
    seq2 = (m,s)
    sequence = s2.join(seq2)


    # collection of different running period of different iteration
    with open(path1 + "/Collection_times.txt", 'a') as f1:
        f1.write(str(sequence))
        f1.write("\n")


    # counting packet loss
    for k in range(1, int(cycles)+1):
        array = []
        with open(path1+"/"+str(k)+"_"+str(p)+".txt", 'r') as f:
            for line in f:
                if "time" in line:
                    if line[0]=='0':
                        array.append(int(line[34:36]))

                    else:
                        array.append(int(line[35:37]))

        result, percentage=err.error(array)

        with open(path1 + "/errorCollection.txt", 'a') as f2:
            f2.write(result)
            f2.write(",")
            f2.write(percentage)
            f2.write("\n")






