import csv

with open('depth.csv') as raw_file:
    file = list(csv.reader(raw_file, delimiter=','))
    depth = tuple(map(lambda l: float(l[1]), file[1::]))

start_size=[]
for i in range(len(depth)):
    if i == 0:
        start = 0
        size = round((depth[0]-depth[1])/2, 1)
        start_size.append((start, size))
        start += size
    elif i != 0 and depth[i] != depth[-1]:
        size = round((depth[i-1]-depth[i+1])/2,1)
        start_size.append((start, size))
        start += size
    else:
        size = round(depth[0] - start - depth[-1])
        start_size.append((start, size))

print(start_size)