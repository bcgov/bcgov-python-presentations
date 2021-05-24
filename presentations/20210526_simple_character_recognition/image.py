'''read ENVI/raw binary format. Dimensions from header, data from .bin file'''
import numpy as np
import matplotlib.pyplot as plt

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

def read_float(fn): # read the raw binary file
    return np.fromfile(fn, dtype = np.float32) / 255. # put data in range [0, 1]

'''pixel @ (row, col) = (i, j):
npx = nrow * ncol # number of pixels in image
red value: dat[          i * ncol + j]
grn value: dat[    npx + i * ncol + j]
blu value: dat[2 * npx + i * ncol + j]'''

def plot(dat, rows, cols, bands, file_name): # plot a "raw binary" format image
    dat = dat.reshape((bands, rows * cols))
    rgb = np.zeros((rows, cols, bands))
    for i in range(bands): rgb[:, :, i] = dat[i, :].reshape((rows, cols))
    plt.imshow(rgb)
    # plt.show() # might need to turn this on to zoom into Figure one to determine line numbers..
    plt.savefig(file_name)
    plt.close()


if __name__ == "__main__":
    dat = [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1,
           0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0,
           0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0]
    rows, cols, bands = 4, 4, 3
    plot(np.array(dat), rows, cols, bands, '4x4.png')  # use this to demonstrate floodfill
