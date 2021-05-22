import os
import sys
import pickle
import numpy as np
from os import walk
import matplotlib.pyplot as plt

def files(path, ext): # get files with specified extension filename.ext
    ret = []
    _, _, filenames = next(walk(path))
    print(filenames)
    for f in filenames:
        if f[-len(ext):] == ext:
            ret.append(f)
    return ret

truth_points = [pickle.load(open('truth' + os.path.sep + f, 'rb')) for f in files('truth', '.p')]
truth_labels = [f.split(os.path.sep)[-1].split('.')[0] for f in files('truth', '.p')]

test_files =  files('test', '.p') # walk can mess up ordering? Walk once
test_points = [pickle.load(open('test' + os.path.sep + f, 'rb')) for f in test_files]
test_centroids = [[float(x) for x in open('test' + os.path.sep + f[:-2] + '.centroid', 'rb').read().strip().split()] for f in test_files]
print("centroids", test_centroids)
'''[[450.62068965517244, 423.4396551724138], [450.0, 502.820987654321], [451.70103092783506, 379.7938144329897], [450.62068965517244, 466.4396551724138], [452.8125, 449.3392857142857], [451.1517857142857, 395.08035714285717], [452.1132075471698, 478.39622641509436], [450.17021276595744, 488.36170212765956], [450.17021276595744, 405.36170212765956], [450.17021276595744, 413.36170212765956], [2014.9074074074074, 849.1111111111111]] '''

# reformat the data
truth_points = [[[x[0] for x in X], [x[1] for x in X]] for X in truth_points]
test_points = [[[x[0] for x in X], [x[1] for x in X]] for X in test_points]

truth_points_by_char = {}
for i in range(len(truth_points)):
    truth_points_by_char[truth_labels[i]] = truth_points[i]

def dist(X, Y):
    subdist = []
    rho, dm, [x1, y1], [x2, y2] = 0, [], X, Y
    i_f_n, j_f_n, arrows = len(x1), len(x2), []
    i_f, j_f = [False for i in range(len(x1))], [False for i in range(len(x2))] # slots for each element compared

    for i in range(0, len(x1)): # calculate sorted distance matrix
        for j in range(0, len(x2)): 
            dm.append([abs(x1[i] - x2[j]) + abs(y1[i] - y2[j]), i, j])

    dm.sort() # sort the array

    # find the distance matrix elements
    for k in range(0, len(dm)):
        d, i, j = dm[k]
        if (not i_f[i]) and (not j_f[j]): # if the slots for both elements compared are open:
            i_f[i], i_f_n, j_f[j], j_f_n, rho = True, i_f_n - 1, True, j_f_n - 1, rho + d # add this term to distance and close the slots
            if d > 0:
                arrows.append([[x1[i], y1[i]], [x2[j], y2[j]]]) # record the stuff on the distance
                subdist.append(d)
        if i_f_n * j_f_n == 0:
            break # ran out of slots for X or Y: stop comparing..

    rho /= min(float(len(x1)), float(len(x2))) # divide by number of slots
    return rho, arrows, subdist

# match onto each character
predictions = [] # list of characters we're trying to infer..

for pi in range(len(test_points)):
    p = test_points[pi]

    # calculate the closest truth value
    min_d, min_i = sys.float_info.max, None   # FLT_MAX in C

    for i in range(len(truth_points)):
        t = truth_points[i]
        d, arrows, subdist = dist(p, t)

        if d < min_d:
            min_d, min_i = d, i

    prediction = truth_labels[min_i]
    predictions.append([test_centroids[pi], prediction])

print("prediction", predictions) # plot distribution of distances, by character!!!!! 

plt.figure()
for p in predictions:
    plt.plot(p[0][1], -p[0][0])
    plt.text(p[0][1], -p[0][0], p[1])
plt.savefig("prediction.png")
