import os
lines = os.popen("ls -1 *.txt  | xargs grep -n n_label").readlines()

d = []
for line in lines:
    line = line.strip()
    k = int(line.split('.')[0].split('_')[1])
    n_class = int(line.split(' ')[-1])
    d.append([k, n_class])

# sort increasing
d.sort(key = lambda x: x[0])
f = open('plot_bear.csv', 'wb')
f.write('n_label,knn_k\n'.encode())
for x in d:
    f.write((str(x[1]) + ',' + str(x[0]) + '\n').encode())
f.close()
