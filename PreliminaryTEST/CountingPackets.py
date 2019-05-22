import Folder as f
import Device
import os


Test="Test2"
bd_addr, bd_name= Device.lines()


c=input("choose part test: )")
if c=="1":
    k=1
    t=6
else:
    k=6
    t=11

c=0
l=[]

path=f.question(str(bd_name),Test)

cycles=input("Enter number of multiple l2ping: ")
path=f.pathTest2(path, cycles)

# counting packets

for p in range(k,t):
    for i in range(1, int(cycles) + 1):
        name_file=(path + "/" + str(i) + "_"+ str(p) + '.txt')
        with open(name_file, 'r') as f1:
            if os.path.getsize(name_file) > 0:
                for line in f1:
                    c=c+1
        l.append(c)
        c=0


ave=sum(l)/len(l)
print(ave)

with open(path+"/countingPacket"".txt", 'w') as f:
    f.write(str(ave))

