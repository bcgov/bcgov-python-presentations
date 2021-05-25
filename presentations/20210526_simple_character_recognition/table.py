''' we used this to generate the table of quivers shown in table.html'''
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
    print("X", X)
    print("Y", Y)
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

    # should probably divide RHO by the number of slots used!!!!
    return rho, arrows, subdist

X_array = [truth_points_by_char[c] for c in ['A','B','C']]
for pi in range(len(X_array)):
    p = X_array[pi]
    for i in range(len(X_array)):
        t = X_array[i]
        print("p", p)
        print("t", t)
        d, arrows, subdist = dist(p, t)

        [x1, y1], [x2, y2] = p, t

        ax, ay, au, av = [], [], [], []
        for a in arrows:
            [sx, sy], [ex, ey] = a # start x,y, end x,y
            ax += [sx]  # arrow starting position
            ay += [sy]
            au += [ex - sx] # arrow delta (flip the direction cuz the direction changes later)
            av += [ey - sy]

        plt.figure()
        plt.scatter(y1, -np.array(x1), color='b') # don't forget to change coordinate conventions.. math [x,y] is graphics [y, -x]
        plt.scatter(y2, -np.array(x2), color='g')
        plt.savefig(str(pi) + "_" + str(i) + ".png")

        plt.figure()
        plt.scatter(y1, -np.array(x1), color='b') # don't forget to change coordinate conventions.. math [x,y] is graphics [y, -x]
        plt.scatter(y2, -np.array(x2), color='g')
        plt.quiver(ay, -np.array(ax), av, -np.array(au), linewidths=10. * np.array(subdist), color='r', angles='xy', scale_units='xy', scale=1.)
        plt.savefig(str(pi) + "_" + str(i) + "_.png")
