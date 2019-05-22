def max_min_average(array):
    max_value="{0:.2f}".format(max_float(array))
    min_value="{0:.2f}".format(min_float(array))
    average_value="{0:.2f}".format(sum(array)/len(array))
    return max_value, min_value, average_value


#compute max float
def max_float(array):
    max_int=0
    max_fraz=0
    i=0

    while i < len(array):
        int_val, fraz_val= float_division(array[i])
        if int_val>max_int:
            max_int=int_val
            max_fraz=fraz_val
        if int_val == max_int:
            if fraz_val>=max_fraz:
                    max_fraz=fraz_val
        i+=1
    result=float_union(max_int,max_fraz)
    return result

#compute min float
def min_float(array):
    min_int = 100000000000
    min_fraz = 100000000000
    i = 0
    while i < len(array):
        int_val, fraz_val = float_division(array[i])
        if int_val<min_int:
            min_int=int_val
            min_fraz=fraz_val
        if int_val == min_int:
            if fraz_val<=min_fraz:
                    min_fraz=fraz_val
        i+= 1
    result = float_union(min_int, min_fraz)
    return result


def float_division(val):
    int_val = int(val)
    fraz_val = (val - int_val) * 100
    return int_val, fraz_val

def float_union(val1, val2):
    value=val1+(val2*0.01)
    return value

def count(file):
    k=0
    f=open(file, 'r')
    for line in f:
        if line!=0:
            k=k+1
    f.close()
    return k-1

