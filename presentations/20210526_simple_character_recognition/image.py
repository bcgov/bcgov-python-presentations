'''read ENVI/raw binary format. Dimensions from header, data from .bin file'''
import os
import sys
import pickle
import numpy as np
from flood import flood
import matplotlib.pyplot as plt
from dist import normalize, to_list, centroid


def read_hdr(hdr):  # read the image dimensions
    cols, rows, bands = 0, 0, 0
    for line in open(hdr).readlines():
        chunks = line.strip().split('=')
        try:  # pull off two chunks delimited by '='
            f, g = [x.strip() for x in chunks[0:2]]
            if f == 'samples':
                cols = g
            if f == 'lines':
                rows = g
            if f == 'bands':
                bands = g
        except:
            pass
    return [int(x) for x in [cols, rows, bands]]  # string to int


def read_float(fn):  # read the raw binary file
    return np.fromfile(fn, dtype=np.float32) / 255.  # put data in range [0, 1]


'''pixel @ (row, col) = (i, j):
npx = nrow * ncol # number of pixels in image
red value: dat[          i * ncol + j]
grn value: dat[    npx + i * ncol + j]
blu value: dat[2 * npx + i * ncol + j]'''


def plot(dat, rows, cols, bands, file_name):  # plot "raw binary" image
    dat = dat.reshape((bands, rows * cols))
    rgb = np.zeros((rows, cols, bands))
    for i in range(bands):
        rgb[:, :, i] = dat[i, :].reshape((rows, cols))
    plt.imshow(rgb)
    # plt.show()  # might uncomment this to zoom in to determine line numbers
    plt.savefig(file_name)
    plt.close()


class image:
    def __init__(self, fn=None):
        if fn:
            self.fn = fn
            self.load(fn)

    def load(self):
        self.cols, self.rows, self.bands = read_hdr(self.fn[:-4] + '.hdr')
        self.dat, self.npx = read_float(self.fn), self.rows * self.cols

    def png(self):
        if type(self.dat) == list:
            self.dat = np.array(self.dat)
        plot(self.dat, self.rows, self.cols, self.bands, self.fn + '.png')

    def gather_points(self):  # list points for each label
        self.points = [[] for i in range(self.next_label)]
        for i in range(self.rows):
            for j in range(self.cols):
                ix = i * self.cols + j  # linear index
                if self.labels[ix] > 0:  # skip background
                    label = self.labels[ix]  # label this point
                    self.points[label] += [[i, j]]

        c = {}  # count the number of pixels per segment
        for point in self.points:
            n = len(point)
            c[n] = (c[n] + 1) if (n in c) else 1

        counts = [[k, c[k]] for k in c]  # sort the counts
        counts.sort()

        ffn = self.fn + '_seg_count.png'
        if not os.path.exists(ffn):
            print('+w ' + ffn)
            plt.figure(figsize=(8, 8))
            fig = plt.barh([str(x[0]) for x in counts],
                           [str(x[1]) for x in counts])
            plt.title("Pixel-count vs. number of segments w that count " +
                      "(total segments: " + str(len(self.points)) + ")")
            plt.xlabel("Number of segments with a given pixel count")
            plt.ylabel("Pixel-count for a segment (total pixel counts = " +
                       str(len(counts)) + ")")
            plt.tight_layout()
            plt.savefig(ffn)
            plt.close()

    def segment(self, flood_lines=None, use_normalize=True):
        print('segment ' + self.fn)
        self.name = self.fn[:-4]
        a = os.system('mkdir -p ' + self.name)
        self.rgb = [[self.dat[i],  # format data into list of rgb tuples
                     self.dat[self.npx + i],
                     self.dat[2 * self.npx + i]] for i in range(0, self.npx)]

        c = {}  # count rgb values
        for x in self.rgb:
            x = str(x)
            c[x] = c[x] + 1 if x in c else 1

        ffn = self.fn + '_rgb_count.png'
        if not os.path.exists(ffn):
            plt.figure()
            plt.bar(c.keys(), np.log(list(c.values())) / np.log(10.))
            plt.title("Log of count of color values")
            print('+w ' + ffn)
            plt.savefig(ffn)
            plt.close()

        counts = [[c[k], k] for k in c]
        counts.sort()
        self.max_color = counts[-1][1]  # assume most-prevalent col is bg

        if sys.getrecursionlimit() < self.npx:  # increase recursion limit
            sys.setrecursionlimit(self.npx)

        # labels for segmentation
        self.labels = [0 for i in range(self.npx)]  # 0 == unlabelled!
        self.next_label = 1

        r_i = flood_lines if flood_lines else range(self.rows)
        for i in r_i:
            for j in range(self.cols):
                flood(self, i, j)
        self.gather_points()  # list (i,j) points by segment

        fn = None
        is_truth = (self.name == 'truth')  # is this truth data?
        truth = None
        if is_truth:
            truth = [x for x in open('truth_chars.txt').read()]

        for pi in range(len(self.points)):  # plot image rep. of each truth
            point = self.points[pi]
            if pi > 0:  # 0 is bg / unlabelled
                try:
                    ns = truth[pi - 1] if is_truth else str(pi)
                    fn = self.name + os.path.sep + ns + '.png'
                    if not os.path.exists(fn):
                        plt.figure()
                        plt.scatter([x[1] for x in point],
                                    [-x[0] for x in point])
                        plt.title(ns)
                        print('+w ' + fn)
                        if not use_normalize:
                            plt.xlim([-.5, self.cols - .5])
                            plt.ylim([-(self.rows - .5), .5])
                        plt.xlabel('col ix')
                        plt.ylabel('-row ix')
                        plt.savefig(fn)
                        plt.close()

                    fn = self.name + os.path.sep + ns + '.centroid'
                    if not os.path.exists(fn):
                        print('  +w ' + fn)
                        xL, yL = to_list(point)
                        cX, cY = centroid(xL, yL)
                        open(fn, 'wb').write((str(cX) + ' ' +
                                              str(cY)).encode())

                    if use_normalize:
                        self.points[pi] = normalize(self.points[pi])

                    # nb run cleanup.py before changing truth inputs
                    fn = self.name + os.path.sep + ns + '.p'
                    if not os.path.exists(fn):
                        print('  +w ' + fn)
                        pickle.dump(point, open(fn, 'wb'))
                except:
                    pass  # don't plot / save the background


if __name__ == "__main__":  # example image data to demonstrate floodfill
    args = sys.argv

    if len(args) < 2:

        dat = [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1,
               0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0,
               0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0]

        a = image()
        a.dat, a.rows, a.cols, a.bands = dat, 4, 4, 3
        a.npx = a.rows * a.cols
        a.fn = '4x4.bin'
        a.png()
        a.segment(use_normalize=False)

    else:
        a = image('truth.bin', [745, 838, 932])
        a.segment()
