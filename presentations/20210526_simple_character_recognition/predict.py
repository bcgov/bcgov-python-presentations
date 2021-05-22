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


test_files = files('test', '.p')
test_points = [pickle.load(open('test' + os.path.sep + f, 'rb')) for f in files('test', '.p')] # don't forget we kept the centroids!

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

# match onto each character!
predictions = []

for pi in range(len(test_points)):
    p = test_points[pi]

    # calculate the closest truth value
    min_d = sys.float_info.max # FLT_MAX in C/C++
    min_i = None

    for i in range(len(truth_points)):
        t = truth_points[i]
        d, arrows, subdist = dist(p, t)

        if d < min_d:
            min_d = d
            min_i = i

    prediction = truth_labels[min_i]
    predictions.append(prediction)

print("prediction", predictions) # plot distribution of distances, by character!!!!! 

# transform the train and test data into the expected format by distance??

# do arrow plots to show how the distance works...

# refer to wasserstein distance?

# don't forget py tesseract..

# last step: partition the pixel patterns into equivalence classes of images (as they're composed of pixels) # notice that the 

# ARCHITECTURE DIAGRAM!!!!! ALGORITHMIC FLOW CHART.......

# big dog style kick the robot.. noise? stretching???
