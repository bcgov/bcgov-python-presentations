import os
import sys
import pickle
import numpy as np
from render import render # LaTeX rendering
import matplotlib.pyplot as plt
from image import read_hdr, read_float, plot
from dist import centroid, normalize, to_list

# untangle the data generation from the segmentation
# untangle the plotting as well!
truth = [x for x in open('truth_chars.txt').read()]  # character repr. of truth data
cols, rows, bands = read_hdr('truth.hdr')  # read truth data image dimensions
dat = read_float('truth.bin')  # read the actual data

# figure1: need to zoom in to determine line numbers (y values) along which to segment
if not os.path.exists('Figure_1.png'):
    plot(dat, rows, cols, bands, 'Figure_1.png')

npx = rows * cols  # number of pixels
rgb = [[dat[i], dat[npx + i], dat[2 * npx + i]] for i in range(0, npx)]  # reformat data into list of (r,g,b) tuples

c = {} # count rgb values
for x in rgb:
    x = str(x)
    c[x] = c[x] + 1 if x in c else 1

if not os.path.exists('Figure_2.png'):
    plt.figure()
    plt.bar(c.keys(), np.log(list(c.values())))
    plt.title("Log of count of color values")
    plt.savefig('Figure_2.png')
    plt.close()

# assume dominant color is bg. Will ignore it in the floodfill
max_count = 0
max_color = None
for k in c:
    if c[k] > max_count:
        max_count, max_color = c[k], k

labels = [0 for i in range(npx)] # starting label: 0 == unlabelled!
next_label = 1

def flood(i, j, my_label = None, my_color = None): # flood-fill segmentation
    global labels, next_label, rgb 
    ix = i * cols + j # linear index of (i, j) 
    if labels[ix] > 0: return # stop: already labelled
    if str(rgb[ix]) == max_color: return # stop: ignore background
    if i > rows or j > cols or i < 0 or j < 0: return  # stop: out of bounds
    if my_color and my_color != str(rgb[ix]): return # stop: different colour than at invocation chain start
 
    if my_label:
        labels[ix] = my_label
    else:
        labels[ix] = next_label
        next_label += 1

    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if not (di == 0 and dj == 0):
                flood(i + di, j + dj, labels[ix], str(rgb[ix]))

if sys.getrecursionlimit() < npx:  # increase recursion limit
    sys.setrecursionlimit(npx)

# this doesn't work because the characters are different heights, this gets them out of order
'''
for i in range(rows):
    for j in range(cols):
        flood(i, j)
'''

# start the segmentation. Cut through the lines for 0-9, a-z, A-Z separately to catch them in order!
i = 745
for j in range(cols): flood(i, j)

i = 838
for j in range(cols): flood(i, j)

i = 932
for j in range(cols): flood(i, j)

def gather_points(labels, next_label, rows, cols):  # list the points for each label
    points = [[] for i in range(next_label)]
    for i in range(rows):
        for j in range(cols):
            ix = i * cols + j # linear index
            if labels[ix] > 0: # skip background
                label = labels[ix] # label this point
                points[label] += [[i, j]]
    return points

points = gather_points(labels, next_label, rows, cols)

c = {}  # count the number of pixels per segment
for point in points:
    n = len(point)
    c[n] = (c[n] + 1) if (n in c) else 1

counts = [[k, c[k]] for k in c] # sort the counts
counts.sort()
print("counts", counts)

# do another bar chart here!!!
if not os.path.exists('Figure_3.png'):
    print("+w Figure_3.png")
    plt.figure(figsize=(8,8))
    fig = plt.barh([str(x[0]) for x in counts], [str(x[1]) for x in counts]) 
    plt.title("Pixel-count vs. number of segments w that count (total segments: " + str(len(points)) + ")")
    plt.xlabel("Number of segments with a given pixel count")
    plt.ylabel("Pixel-count for a segment (total pixel counts = " + str(len(counts)) + ")")
    plt.tight_layout()
    plt.savefig('Figure_3.png')
    plt.close()

for i in range(len(points)): # apply centroid adjust
    points[i] = normalize(points[i]) 

ci = 0
truth_points = {} # index the point sets by the character type representation
for point in points:  # plot image rep. of each "truth" data character, in an appropriately labelled file
    if ci > 0:
        try:
            truth_label = truth[ci - 1]
            fn = 'truth' + os.path.sep + truth_label + '.png'
            if not os.path.exists(fn):
                plt.figure()
                plt.scatter([x[1] for x in point], [-x[0] for x in point])  # scatter plot of within-segment (x,y) pixel coords
                truth_points[truth_label] = point  # retain a lookup
                plt.title(truth_label)
                print('+w ' + fn)
                plt.savefig(fn)
                plt.close()

            fn = 'truth' + os.path.sep + truth_label + '.p'  # save (x,y) coords for this glyph, in pickle file to restore later
            if not os.path.exists(fn):
                pickle.dump(point, open(fn, 'wb'))  # n.b. need to run cleanup.py to regenerate truth / test data
        except:
            pass  # don't plot / save the background
    ci += 1

print(truth)

print("read test data..")
cols, rows, bands = read_hdr('test.hdr')
dat = read_float('test.bin') 

if not os.path.exists('Figure_4.png'):
    plot(dat, rows, cols, bands, 'Figure_4.png') 

npx = rows * cols
rgb = [[dat[i], dat[npx + i], dat[2 * npx + i]] for i in range(0, npx)]

c = {} # count rgb values
for x in rgb:
    x = str(x)
    c[x] = c[x] + 1 if x in c else 1
# print(c)

if not os.path.exists('Figure_5.png'):
    plt.figure()
    plt.bar(c.keys(), np.log(list(c.values())))
    plt.title("Log of count of color values")
    plt.savefig('Figure_5.png')
    plt.close()

# assume dominant color is background
max_count = 0
max_color = None
for k in c:
    if c[k] > max_count:
        max_count, max_color = c[k], k

labels, next_label = [0 for i in range(npx)], 1 # starting label: 0 == unlabelled!

print("floodfill test data..")
for i in range(rows):
    for j in range(cols):
        flood(i, j)

print("next_label", next_label)

points = gather_points(labels, next_label, rows, cols)

c = {}
for point in points:
    n = len(point)
    c[n] = (c[n] + 1) if (n in c) else 1

counts = [[k, c[k]] for k in c] # sort the counts
counts.sort()
print("counts", counts)

# do another bar chart here!!!
if not os.path.exists('Figure_6.png'):
    print("+w Figure_6.png")
    plt.figure(figsize=(8,8))
    fig = plt.barh([str(x[0]) for x in counts], [str(x[1]) for x in counts]) 
    plt.title("Pixel-count vs. number of segments w that count (total segments: " + str(len(points)) + ")")
    plt.xlabel("Number of segments with a given pixel count")
    plt.ylabel("Pixel-count for a segment (total pixel counts = " + str(len(counts)) + ")")
    plt.tight_layout()
    plt.savefig('Figure_6.png')
    plt.close()

ci, test_points = 0, {} # point sets indexed by the character-type representation
for point in points:
    if ci > 0:
        try:
            fn = 'test' + os.path.sep + str(ci) + '.png'
            if not os.path.exists(fn):
                plt.figure()
                plt.scatter([x[1] for x in point], [-x[0] for x in point])
                plt.title('test_' + str(ci)) # truth_label)
                print('+w ' + fn)
                plt.savefig(fn)
                plt.close()

            fn = 'test' + os.path.sep + str(ci) + '.centroid'  # record centroid for "reconstruction". Why? Glyphs not equal size. Faller glyphs come out first! 
            if not os.path.exists(fn):
                xL, yL = to_list(point)
                cX, cY = centroid(xL, yL)
                open(fn, 'wb').write((str(cX) + ' ' + str(cY)).encode())
                
            point = normalize(point) # centroid adjustment, subtract average x,y coords

            fn = 'test' + os.path.sep + str(ci) + '.p'  # save the glyph's points, in pickle file to restore later
            if not os.path.exists(fn):
                pickle.dump(point, open(fn, 'wb'))
        except:
            pass  # don't plot / save the background
    ci += 1
