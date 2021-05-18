import os

def run(c): # run something at terminal and wait to finish
    a = os.system(c)

def chars(i, j):
    return ' '.join([chr(x) for x in range(i, j)])

open('train.tex', 'wb').write(('\n'.join(['\\documentclass{letter}',
                                         '\\usepackage{xcolor}',
                                         '\\begin{document}',
                                         '\\color{blue}',
                                         chars(48, 58) + '\n', # 0-9
                                         chars(65, 91) + '\n', # A-Z
                                         chars(97, 123), # a-z
                                         '\\end{document}'])).encode())

run('pdflatex train.tex') # render with LaTeX
run('convert -background white -density 200 train.pdf train.bmp') # convert to png
run('gdal_translate -of ENVI -ot Float32 train.bmp train.bin') # convert to raw binary

# add band names
d = open("test.hdr").read() + 'band names = {red,\ngreen,\nblue}'
open('test.hdr','wb').write(d.encode())


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
red value: dat[0 * npx + i * ncol + j]
grn value: dat[1 * npx + i * ncol + j]
blu value: dat[2 * npx + i * ncol + j]'''
dat = read_float("test.bin")

def plot(dat, rows, cols, bands):
    dat = dat.reshape((bands, rows * cols))
    rgb = np.zeros((rows, cols, bands))

    for i in range(bands):
         rgb[:, :, i] = dat[i, :].reshape((rows, cols))
    
    import matplotlib.pyplot as plt

    plt.imshow(rgb)
    plt.show()

plot(dat, rows, cols, bands)
