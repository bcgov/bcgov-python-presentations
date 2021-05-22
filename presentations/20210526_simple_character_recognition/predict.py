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

truth_points = [[[x[0] for x in X], [x[1] for x in X]] for X in truth_points]
test_points = [[[x[0] for x in X], [x[1] for x in X]] for X in test_points]

def dist(X, Y):
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
            arrows.append([[x1[i], y1[i]], [x2[j], y2[j]]]) # record the stuff on the distance
        if i_f_n * j_f_n == 0:
            break # what does this mean???
    return rho, arrows

for pi in range(len(test_points)):
    p = test_points[pi]
    for i in range(0, len(truth_points)):
        t = truth_points[i]
        d, arrows = dist(p, t)

        [x1, y1], [x2, y2] = p, t

        plt.figure()
        plt.scatter(y1, -np.array(x1), color='b')
        plt.scatter(y2, -np.array(x2), color='r')
        plt.show()

        '''if d==0:
            print("train_label", truth_labels[i])
            os.system("eog test/" + test_files[pi][:-2] +'.png')
        '''
    sys.exit(1)



'''
o_f, r_i, n_glyph = open("outfile" + str(ci) + ".ext", "wb"), 0, len(px)
for ix in px:
    r_i += 1
    if len(px[ix]) > a and len(px[ix]) < b: #print ix, '->', px[ix]
        x, y = [], []
        for p in px[ix]:
            i, j = p.split(",")
            x.append(float(j)); y.append(-float(i))
        xb, yb = np.mean(x), np.mean(y) # we shouldn't do this twice! scratch this later..
        x, y = [i - xb for i in x], [i - yb for i in y]
        ci, d_min, c_min = 0, None, None
        for c in chars:
            d, ci = dist([x,y], truth[c]), ci + 1  # should use set builder notation on this?
            d_min, c_min = d if ci == 1 else d_min,  c if ci == 1 else c_min
            if d < d_min: d_min, c_min = d, c
        if d_min > 0.1: print(c_min, "d= %.1f" % d_min, "r=", r_i, "/", n_glyph)
        if d_min > 2.:
            if r_i > 111:
                break
        o_f.write(c_min.encode('ascii'))
o_f.close()

# these last two lines commented out because we already (re)named..
#if len(sys.argv) > 1:
#    a = os.system("cp -v outfile.ext outfile"+str(sys.argv[1])+".ext")

'''
print("done parse")

# transform the train and test data into the expected format by distance??

# do arrow plots to show how the distance works...

# refer to wasserstein distance?

# don't forget py tesseract..

# last step: partition the pixel patterns into equivalence classes of images (as they're composed of pixels) # notice that the 

# ARCHITECTURE DIAGRAM!!!!!
