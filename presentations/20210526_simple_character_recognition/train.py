import os

def run(c): # run something at terminal and wait to finish
    a = os.system(c)

truth = []

def chars(i, j):
    global truth
    my_chars = [chr(x) for x in range(i, j)]
    truth += my_chars
    return ' '.join(my_chars)

open('train.tex', 'wb').write(('\n'.join(['\\documentclass{letter}',
                                         '\\usepackage{xcolor}',
                                         '\\begin{document}',
                                         '\\color{blue}',
                                         chars(48, 58) + '\n', # 0-9
                                         chars(65, 91) + '\n', # A-Z
                                         chars(97, 123),       # a-z
                                         '\\end{document}'])).encode())

if not os.path.exists('train.bin'): # delete train.bin to start from new data
    run('pdflatex train.tex') # render with LaTeX
    run('convert -background white -density 200 train.pdf train.bmp') # convert to bitmap
    run('gdal_translate -of ENVI -ot Float32 train.bmp train.bin') # convert to raw binary

# add band names
d = open("train.hdr").read() + 'band names = {red,\ngreen,\nblue}'
open('train.hdr','wb').write(d.encode())


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

cols, rows, bands = read_hdr("test.hdr")


'''pixel @ (row, col) = (i, j):
npx = nrow * ncol # number of pixels in image
red value: dat[          i * ncol + j]
grn value: dat[    npx + i * ncol + j]
blu value: dat[2 * npx + i * ncol + j]'''

dat = read_float("test.bin") / 255.

import matplotlib.pyplot as plt

def plot(dat, rows, cols, bands, file_name): # plot a "raw binary" format image
    dat = dat.reshape((bands, rows * cols))
    rgb = np.zeros((rows, cols, bands))
    for i in range(bands):
        rgb[:, :, i] = dat[i, :].reshape((rows, cols))
    plt.imshow(rgb)
    plt.savefig(file_name)

plot(dat, rows, cols, bands, 'Figure_1.png') # Figure 1

# basic color stats
npx = rows * cols
rgb = [[dat[i], dat[npx + i], dat[2 * npx + i]] for i in range(0, npx)]

c = {} # count rgb values
for x in rgb:
    x = str(x)
    c[x] = c[x] + 1 if x in c else 1
print(c)

'''
{'[255.0, 255.0, 255.0]': 3732995,
 '[0.0, 0.0, 255.0]': 6951,
 '[0.0, 0.0, 0.0]': 54} 

'''

plt.figure()
plt.bar(c.keys(), np.log(list(c.values())))
plt.title("Log of count of color values")
plt.savefig('Figure_2.png')

labels = np.zeros(npx) # starting label: 0 == unlabelled!
next_label = 1

def flood(i, j, my_label = None, my_color = None): # flood-fill segmentation
    ix = i * cols + j # linear index of (i, j) 
    if labels[ix] > 0: return  # stop: already labelled
    if i > rows or j > cols or i < 0 or j < 0: return  # stop: out of bounds
    if my_color and my_color != str(rgb[ix]): return # stop: different colour than at invocation chain start

    # label this point
    labels[ix] = my_label if my_label else next_label
    next_label = next_label if my_label else next_label + 1

    for di in [-1, 1]:
        for dj in [-1, 1]:
            find(i + di, j + dj, labels[ix], str(rgb[i, j]))
    

    if labels[i, j] > 0: # "base case"!
        return labels[i, j] # already labelled

    for di in [-1, 1]: # +-shaped nbhd!
        for dj in [-1, 1]:
            find(i + di, j + dj, labels[ix], str(rgb[ix]))


for i in range(rows):
    for j in range(cols):
        flood(i, j)

print(labels)
print(next_label)



# don't forget py tesseract..
