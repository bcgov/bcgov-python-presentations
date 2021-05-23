'''quasi earth-mover distance..
.. put simple examples in here? in main? '''
import numpy as np

def to_list(A): # convert list of [x,y] points to separate lists for x, y
    return [[x[0] for x in A], [x[1] for x in A]]

def centroid(X, Y):  # mean of x, y coordinate lists..
    return [np.mean(X), np.mean(Y)]

def normalize(A):  # normalize a list of [x,y] points.. subtract centroid
    X, Y = to_list(A)
    cX, cY = centroid(X, Y)
    return [[X[i] - cX, Y[i] - cY] for i in range(len(A))]

def dist(X, Y):
    rho, [x1, y1], [x2, y2] = 0, X, Y  # compare two point-sets
    i_f_n, j_f_n = len(x1), len(x2)
    subdist, arrows = [], []  # for visualization only
    i_f, j_f = [False for i in range(len(x1))], [False for i in range(len(x2))] # element-wise slots for element-inclusion in traffic plan

    dm = [[abs(x1[i] - x2[j]) + abs(y1[i] - y2[j]), i, j] for i in range(len(x1)) for j in range(len(x2))]  # distance matrix
    dm.sort() # sort the matrix

    for k in range(len(dm)): # dmat elements
        d, i, j = dm[k]  # distance btwn points, indices of points compared..
        if not i_f[i] and not j_f[j]: # if slots open for both elements:
            i_f[i], i_f_n, j_f[j], j_f_n, rho = True, i_f_n - 1, True, j_f_n - 1, rho + d # add this term to distance and close the slots
            if d > 0:  # record stuff for visualization
                arrows.append([[x1[i], y1[i]], [x2[j], y2[j]]])
                subdist.append(d)

        if i_f_n * j_f_n == 0:
            break # ran out of slots for X or Y: stop comparing..

    rho /= min(float(len(x1)), float(len(x2))) # divide by number of slots
    return rho, arrows, subdist
