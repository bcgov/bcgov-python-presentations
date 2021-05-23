# add argparse
import os
import sys
import pickle
import numpy as np
from os import walk
import multiprocessing as mp
import matplotlib.pyplot as plt
from dist import dist # our distance

def files(path, ext): # get files with specified extension filename.ext
    ret = []
    _, _, filenames = next(walk(path))
    for f in filenames:
        if f[-len(ext):] == ext:
            ret.append(f)
    return ret

truth_files = files('truth', '.p')  # load truth data
truth_labels = [f.split(os.path.sep)[-1].split('.')[0] for f in truth_files]
truth_points = [pickle.load(open('truth' + os.path.sep + f, 'rb')) for f in truth_files]

test_files =  files('test', '.p') # load test data. Walk can mess up ordering if called on different extensions? Walk once
test_points = [pickle.load(open('test' + os.path.sep + f, 'rb')) for f in test_files]
test_centroids = [[float(x) for x in open('test' + os.path.sep + f[:-2] + '.centroid', 'rb').read().strip().split()] for f in test_files]
print("centroids", test_centroids)

test_points = [[[x[0] for x in X], [x[1] for x in X]] for X in test_points] # reformat the data
truth_points = [[[x[0] for x in X], [x[1] for x in X]] for X in truth_points]

# mapping to find the index of a given character in the list of truth-data points..
truth_points_by_char = {truth_labels[i]: truth_points[i] for i in range(len(truth_points))}
   
# match onto each character
predictions = [] # list of characters we're trying to infer..

def parfor(my_func, my_in): # parallel for loop
    return mp.Pool(mp.cpu_count()).map(my_func, my_in)

def predict_i(pi): # for pi in range(len(test_points)):
    print(test_files[pi])
    p = test_points[pi]

    min_d, min_i = sys.float_info.max, None  # distance and index of closest truth value

    for i in range(len(truth_points)):
        t = truth_points[i]
        d, arrows, subdist = dist(p, t)
        print("rho", d, "i", i)

        if d < min_d: # found a better match
            min_d, min_i = d, i

        if min_d == 0.: # perfect match, stop looking..
            break 

    print("min_i", min_i)
    prediction = truth_labels[min_i]
    result = [test_centroids[pi], prediction]
    print(result)
    return(result)
    print("point", pi, "of", len(test_points))

print("truth_points", truth_points)

use_parfor = True
if use_parfor:
    predictions = parfor(predict_i, range(len(test_points)))
else:
    predictions = [predict_i(pi) for pi in range(len(test_points))]

print("prediction", predictions) # plot distribution of distances, by character!!!!! 

plt.figure()
for p in predictions:
    plt.plot(p[0][1], -p[0][0])
    plt.text(p[0][1], -p[0][0], p[1])
plt.show()
plt.savefig("prediction.png")


# CHARACTER - IZE / EYES!!!
