# convert envi format image file (.bin) to .csv
# python3 envi_to_csv.py  bear.bin  >  example_02_bear.csv
import os
import sys
import numpy as np
args, exists = sys.argv, os.path.exists

def err(m):
    print("Error:", m)
    sys.exit(1)

# use numpy to read a floating-point data file (4 bytes per float, byte order 0)
def read_float(fn):
    # print("+r", fn)
    return np.fromfile(fn, '<f4')

def read_hdr(hdr):
    samples, lines, bands = 0, 0, 0
    for line in open(hdr).readlines():
        words = line.strip().split('=')
        if len(words) == 2:
            f, g = words[0].strip(), words[1].strip()
            if f == 'samples': samples = int(g)
            if f == 'lines': lines = int(g)
            if f == 'bands': bands = int(g)
    return samples, lines, bands

fn = args[1]
if not exists(fn):
    err('failed to find input file: ' + fn)
if fn[-3:] != 'bin':
    err('bin file expected')

hfn = fn[:-3] + 'hdr'
if not exists(hfn):
    err('failed to find hdr file: ' + hfn)

nc, nr, nb = read_hdr(hfn)  # n cols, n rows, n bands: >3d supported
dat = read_float(fn)
np = nr * nc
bands = range(0, nb)
print(','.join([str(k) for k in bands]))
for i in range(0, np):
    pixel = [dat[k * np + i] for k in bands]
    print(','.join([str(pixel[k]) for k in bands]))
