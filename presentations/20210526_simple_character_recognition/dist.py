'''quasi earth-mover distance'''
import numpy as np


def to_list(A):  # convert list of [x,y] points to separate lists for x, y
    return [[x[0] for x in A], [x[1] for x in A]]


def centroid(X, Y):  # mean of x, y coordinate lists..
    return [np.mean(X), np.mean(Y)]


def normalize(A):  # normalize a list of [x,y] points.. subtract centroid
    X, Y = to_list(A)
    cX, cY = centroid(X, Y)
    return [[X[i] - cX, Y[i] - cY] for i in range(len(A))]


def dist(X, Y):
    rho, [x1, y1], [x2, y2] = 0, X, Y  # compare two point-sets
    i_n, j_n = len(x1), len(x2)
    subdist, arrows = [], []  # for visualization only

    # element-wise slots for inclusion of each element in traffic plan
    i_f, j_f = [False for i in range(i_n)], [False for i in range(j_n)]

    dm = [[abs(x1[i] - x2[j]) + abs(y1[i] - y2[j]), i, j]
          for i in range(i_n) for j in range(j_n)]  # distance matrix
    dm.sort()  # sorted distance matrix

    for k in range(len(dm)):  # for each dmat element
        d, i, j = dm[k]  # dist btwn points, indices of points compared

        if not i_f[i] and not j_f[j]:  # if slots open for both elements:

            # add term to distance and close the slots
            i_f[i], i_n, j_f[j], j_n, rho = [True,
                                             i_n - 1,
                                             True,
                                             j_n - 1,
                                             rho + d]

            if d > 0:  # record stuff for visualization
                arrows.append([[x1[i], y1[i]], [x2[j], y2[j]]])
                subdist.append(d)

        if i_n * j_n == 0:
            break  # ran out of slots for X or Y: stop comparing..

    rho /= len(arrows)  # divide by the number of slots
    return rho, arrows, subdist
