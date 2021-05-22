import sys
mypath = "test"
from os import walk

def files(path, ext):
    ret = []
    _, _, filenames = next(walk(mypath))
    print(filenames)
    for f in filenames:
        if f[-len(ext):] == ext:
            ret.append(f)
    return ret

train_points = [pickle.load(f) for f in files('truth', '.p')]
test_points = [pickle.load(f) for f in files('train', '.p')]


sys.exit(1)

def dist(X, Y):
    # assume already centroid adjusted?
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
