import os

import mathmath as mat

def standard(bd_addr, path,i):

    #   l2ping
    namefile=str(i)
    os.system("sudo l2ping -s 44 "+ bd_addr + " >" + path+ "/"+ namefile+ '.txt')


    #   Computation max min and average
    with open(path+"/collected_results.txt", 'a') as f:
        max_value, min_value, average_value=readingPing(path, namefile)

        s2 = " "
        seq2 = (str(max_value), str(min_value), str(average_value))
        sequence = s2.join(seq2)
        f.write("{}\n".format(sequence))

    #   Counting of Ping before that the connection fall down
    with open(path + "/CountingPing_collection.txt", 'a') as f1:
        count=mat.count(path + "/"+ namefile+ '.txt')
        f1.write(str(count))
        f1.write("\n")



def flood(bd_addr, path, namefile, i):

    #l2ping flood

    os.system("sudo l2ping -f " + bd_addr + " >" + path + "/" + str(namefile) + "_"+ str(i) + '.txt')



#reading of the file, writing on an array, computing ov max/min/ave of the value in the arrey, return max/min/ave
def readingPing(path, namefile):
    time_array = []
    ms_string = []
    with open(path+ "/" + namefile+ ".txt") as f:
        for line in f:
            if "time" in line:
                if line[0]!='0':
                    time_array.append(line[42:])
                    ms_string.append(float(line[42:-3]))
                else:
                    time_array.append(line[41:])
                    ms_string.append(float(line[41:-3]))

    max_value, min_value, average_value = mat.max_min_average(ms_string)
    return max_value, min_value, average_value