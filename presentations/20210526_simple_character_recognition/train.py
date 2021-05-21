import os
import sys

def run(c): # run something at terminal and wait to finish
    print(c)
    a = os.system(c)

truth = [] # these are the characters we'd like to classify

def chars(i, j):
    global truth
    my_chars = [chr(x) for x in range(i, j)]
    truth += my_chars
    return ' '.join(my_chars)

my_text = [chars(48, 58) + '\n', # 0-9
           chars(65, 91) + '\n', # A-Z
           chars(97, 123)]       # a-z

def render(my_text, name='train'):
    # use "Computer Modern" font by Donald Knuth # insert Knuth quotes..
    open(name + '.tex', 'wb').write(('\n'.join(['\\documentclass{letter}',
                                                '\\usepackage{xcolor}',
                                                '\\begin{document}',
                                                '\\color{blue}'] +
                                                my_text + 
                                                ['\\end{document}'])).encode())

    if not os.path.exists(name + '.bin'): # delete train.bin to start from new data
        run('pdflatex ' + name + '.tex') # render with LaTeX
        run('convert -background white -density 200 ' + name + '.pdf ' + name + '.bmp') # convert to bitmap
        run('gdal_translate -of ENVI -ot Float32 ' + name + '.bmp ' + name + '.bin') # convert to raw binary
        
        if os.path.exists(name + '.hdr'):
            # add band names
            d = open(name + '.hdr').read() + 'band names = {red,\ngreen,\nblue}'
            open(name + '.hdr','wb').write(d.encode())

render(my_text)


def read_hdr(hdr): # read the image dimensions
    cols, rows, bands = 0, 0, 0
    for line in open(hdr).readlines():
        chunks = line.strip().split('=')
        try: # pull off two chunks delimited by '='
            f, g = [x.strip() for x in chunks[0:2]]
            if f == 'samples': cols = g
            if f == 'lines': rows = g
            if f == 'bands': bands = g
        except:
            pass
    return [int(x) for x in [cols, rows, bands]] # string to int

import numpy as np

def read_float(fn): # read the raw binary file
    return np.fromfile(fn, dtype = np.float32)

cols, rows, bands = read_hdr('train.hdr')


'''pixel @ (row, col) = (i, j):
npx = nrow * ncol # number of pixels in image
red value: dat[          i * ncol + j]
grn value: dat[    npx + i * ncol + j]
blu value: dat[2 * npx + i * ncol + j]'''

dat = read_float('train.bin') / 255.

import matplotlib.pyplot as plt

def plot(dat, rows, cols, bands, file_name): # plot a "raw binary" format image
    dat = dat.reshape((bands, rows * cols))
    rgb = np.zeros((rows, cols, bands))
    for i in range(bands):
        rgb[:, :, i] = dat[i, :].reshape((rows, cols))
    plt.imshow(rgb)
    plt.savefig(file_name)
    plt.close()

if not os.path.exists('Figure_1.png'):
    plot(dat, rows, cols, bands, 'Figure_1.png') # Figure 1

# basic color stats
npx = rows * cols
rgb = [[dat[i], dat[npx + i], dat[2 * npx + i]] for i in range(0, npx)]

c = {} # count rgb values
for x in rgb:
    x = str(x)
    c[x] = c[x] + 1 if x in c else 1
# print(c)

'''
{'[255.0, 255.0, 255.0]': 3732995,
 '[0.0, 0.0, 255.0]': 6951,
 '[0.0, 0.0, 0.0]': 54} 

'''

if not os.path.exists('Figure_2.png'):
    plt.figure()
    plt.bar(c.keys(), np.log(list(c.values())))
    plt.title("Log of count of color values")
    plt.savefig('Figure_2.png')
    plt.close()

# assume dominant color is background
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

# start the segmentation
i = 450
for j in range(cols):
    flood(i, j)

i = 500
for j in range(cols):
    flood(i, j)

i = 560
for j in range(cols):
    flood(i, j)

# print(labels)
# print(next_label)

points = [[] for i in range(next_label)]

# gather the points for each label
for i in range(rows):
    # print(i, rows)
    for j in range(cols):
        ix = i * cols + j # linear index
        if labels[ix] > 0: # skip background
            label = labels[ix] # label this point
            points[label] += [[i, j]]


# for point in points:
#     print(len(point))

c = {}
for point in points:
    n = len(point)
    c[n] = (c[n] + 1) if (n in c) else 1

counts = [[k, c[k]] for k in c] # sort the counts
counts.sort()
print(counts)

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

# centroid adjustment
def normalize(A):
    X = [x[0] for x in A]
    Y = [x[1] for x in A]
    cX, cY = np.mean(X), np.mean(Y)
    return [[X[i] - cX, Y[i] - cY] for i in range(len(A))]

for i in range(len(points)): # apply centroid adjust # WRITE OUT IN MATH?
    points[i] = normalize(points[i]) 

run("mkdir -p truth")
ci = 0
truth_points = {} # index the point sets by the character type representation
for point in points:
    if ci > 0:
        try:
            plt.figure()
            truth_label = truth[ci - 1]
            fn = 'truth' + os.path.sep + truth_label + '.png'
            plt.scatter([x[1] for x in point], [-x[0] for x in point])
            truth_points[truth_label] = point
            plt.title(truth_label)
            print('+w ' + fn)
            plt.savefig(fn)
            plt.close()
        except:
            pass
    ci += 1

print(truth)

def dist(X, Y):
    # assume already centroid adjusted
    # [x1, y1], [x2, y2]= normalize(X), normalize(Y) # centroid adjust
    rho, dm, i_f_n, j_f_n = 0., [], [], [], len(x1), len(x2)
    i_f, j_f = [False for i in range(len(x1))], [False for i in range(len(x2))]
    for i in range(0, len(x1)):
        for j in range(0, len(x2)):
            dm.append([abs(x1[i] - x2[j]) + abs(y1[i] - y2[j]), i, j])
    dm.sort() # sort the array
    for k in range(0, len(dm)):
        d, i, j = dm[k]
        if (not i_f[i]) and (not j_f[j]):
            i_f[i], i_f_n, j_f[j], j_f_n, rho = True, i_f_n - 1, True, j_f_n - 1, rho + d
        # print(rho, d, i, j) # study the probability of this changing. If unlikely to change, quit.
        # Poisson? look at profiles of rho! A really interesting distribution
        if i_f_n * j_f_n == 0: break
    return rho


render(["h3ll0 w0rlD"], "test")

dat = read_float('test.bin') / 255.

# transform the train and test data into the expected format by distance??
# do arrow plots to show how the distance works...
# refer to wasserstein distance?

# don't forget py tesseract..
