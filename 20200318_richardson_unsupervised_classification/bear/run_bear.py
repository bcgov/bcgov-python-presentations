# run bear example with knn_k at different values
import os
cmd = 'python3 ../kgc.py bear.csv '
for i in range(10, 1111, 10):
    c = cmd + str(i) + ' 1 > bear_' + str(i) + '.txt'
    print(c)
    # a = os.system(cmd)
