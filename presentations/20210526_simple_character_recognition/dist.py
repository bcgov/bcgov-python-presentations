'''quasi earth-mover distance'''
import numpy as np
import matplotlib.pyplot as plt

def to_list(A):  # convert list of [x,y] points to separate lists for x, y
    return [[x[0] for x in A], [x[1] for x in A]]


def centroid(X, Y):  # mean of x, y coordinate lists..
    return [np.mean(X), np.mean(Y)]


def normalize(A):  # subtract centroid
    X, Y = A
    I = range(len(X))
    cX, cY = centroid(X, Y)
    return [X[i] - cX for i in I], [Y[i] - cY for i in I]

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

    rho /= min(float(len(x1)), float(len(x2)))  # divide by the number of slots
    return rho, arrows, subdist


def dist_plot(X, Y, d, arrows, subdist, i, j):
    [x1, y1], [x2, y2] = X, Y
    ax, ay, au, av = [], [], [], []
    for a in arrows:
        [sx, sy], [ex, ey] = a # start x,y, end x,y
        ax += [sx]  # arrow starting position
        ay += [sy]
        au += [ex - sx] # arrow delta (flip the direction cuz the direction changes later)
        av += [ey - sy]

    if False:
        plt.figure()
        plt.scatter(y1, -np.array(x1), color='b') # don't forget to change coordinate conventions.. math [x,y] is graphics [y, -x]
        plt.scatter(y2, -np.array(x2), color='g')
        plt.savefig(str(i) + "_" + str(j) + ".png")

    plt.figure()
    plt.scatter(y1, -np.array(x1), color='b') # don't forget to change coordinate conventions.. math [x,y] is graphics [y, -x]
    plt.scatter(y2, -np.array(x2), color='g')
    # plt.scatter(ax, ay, color='r')
    plt.quiver(ay, -np.array(ax), av, -np.array(au), linewidths=10. * np.array(subdist), color='r', angles='xy', scale_units='xy', scale=1.) # -np.array( au), -np.array(av), color = 'r') # ay, -np.array(ax), av, np.array(au), color='r')
    # plt.show()
    plt.savefig('dist_' + str(i) + "_" + str(j) + "_.png")
    plt.close()


'''put in a command line plot here to calculate distances between things (put the diagrams on for this case.. but not the predict case'''
