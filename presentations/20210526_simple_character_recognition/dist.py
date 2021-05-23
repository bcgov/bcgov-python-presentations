'''
quasi earth-mover distance..
.. put simple examples in here? in main?
'''
def dist(X, Y):
    rho, [x1, y1], [x2, y2] = 0, X, Y
    i_f_n, j_f_n = len(x1), len(x2)
    subdist, arrows = [], []
    i_f = [False for i in range(len(x1))]
    j_f = [False for i in range(len(x2))] # slots for each element's inclusion in traffic plan
    dm = [[abs(x1[i] - x2[j]) + abs(y1[i] - y2[j]), i, j] for i in range(len(x1)) for j in range(len(x2))]
    dm.sort() # sort the matrix

    for k in range(0, len(dm)): # dmat elements
        d, i, j = dm[k]
        if (not i_f[i]) and (not j_f[j]): # if the slots for both elements compared are open:
            i_f[i], i_f_n, j_f[j], j_f_n, rho = True, i_f_n - 1, True, j_f_n - 1, rho + d # add this term to distance and close the slots
            if d > 0:
                arrows.append([[x1[i], y1[i]], [x2[j], y2[j]]]) # record the stuff on the distance
                subdist.append(d)
        if i_f_n * j_f_n == 0: break # ran out of slots for X or Y: stop comparing..

    rho /= min(float(len(x1)), float(len(x2))) # divide by number of slots
    return rho, arrows, subdist
