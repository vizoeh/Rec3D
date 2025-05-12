import csv
import numpy as np

with open('depth.csv') as raw_file:
    file = list(csv.reader(raw_file, delimiter=','))
    depth = tuple(map(lambda l: int(float(l[1])*10), file[1::]))

print(depth)

start = 0
start_size=[]
for i in range(len(depth)):
    if i == 0:
        print(start)
        start = 0
        size = int(round((depth[0]-depth[1])/2, 0))
        start_size.append((start, size))
        start += size
    elif i != 0 and depth[i] != depth[-1]:
        print(start)
        size = int(round((depth[i-1]-depth[i+1])/2,0))
        start_size.append((start, size))
        start += size
    else:
        print(start)
        size = int(round(depth[0] - start - depth[-1]))
        start_size.append((start, size))

print(start_size)