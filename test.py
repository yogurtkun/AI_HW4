from driver_3 import tuple2index,index2tuple,list_copy

a = [(0,set([1,2])),(1,set([4,5]))]

def f(d):
    d[0][1].add(10)

b = list_copy(a)
f(b)

print(a)