def error(array):
    k=0
    l=0
    for i in range(0,len(array)):
        if k==array[i]:
            l=l+1
        if k!=array[i]:
            k=array[i]
        k=k+1
        if k==55:
            k=0



    #print(l)

    if l==len(array):
        result="0 errors"
        percentage="0%"

    else:
        err=len(array)-l
        result=str(err)+" errors"
        percentage=str((l*100)/len(array)) + "%"

    return result, percentage


