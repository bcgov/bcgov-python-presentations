# 20200317 implementation of KGC (2010) unsupervised classifier
from util import *

'''variables for clustering'''
data = None  #  1. Input data         a) points
idx = None  #                         b) range(0, len(data))
knn_k = None  # 2. Intermediate data: a) number of k-nearest neighbours
dmat = None  #                        b) list of rows of sorted dist. matrix
rho = None  #   3. Model data         a) density estimate
label = None  # 4. Class data         a) class label
next_label = None   #                 b) next avail. class label
class_label = None  #                 c) truth data label if available!

# command line parameters
input_file = None
print("len(args)", len(args), "args", str(args))

if len(args) > 1:
    input_file = args[1]
    print("input_file", input_file)
else:
    err("Error:\n\tusage: python3 kgc.py [input file name] [knn-k (optional)]")

if len(args) > 2:
    knn_k = int(args[2])
    print("knn_k", knn_k)

# other parameters
scale_data = len(args) > 3  # add an optional parameter to turn on [0, 1] scaling

# calculate one sorted row of the distance matrix
def dmat_row(i):
    global data, idx
    row, pi, n_d = [], data[i], len(data[i]) 

    for j in idx:
        d, pj = 0., data[j]  # d(data[i], data[j]), data[j]
        for k in range(0, n_d):
            d += math.pow(pi[k] - pj[k], 2)
        row.append([d, j])

    # print(row)
    row.sort(key=lambda x: x[0]) # sort on dist: increasing
    # print(row)
    return row  # output: sorted dmat row for data[i]


def rho(): # density estimation
    global data, idx, knn_k, dmat, rho
    rho = []
    for i in idx:  # for each point
        row, r = dmat[i], 0.  # distance matrix row, dens. est. for a point
        for j in range(0, knn_k):
            r += row[j][0] # add dist. to j-th nearest neighbour 
        try: rho.append(1. / r)
        except Exception: pass

def climb(i, climb_from = None):
    print("climb i=", i, "from", climb_from)
    global rho, knn_k, dmat, label, next_label

    if label[i] >= 0:
        return label[i]  # base case: data[i] already done
    else:
        dmat_row = dmat[i]

        rho_knn = [[rho[j], j] # [density estimate, data idx j]
                   for j in [dmat_row[k][1] # for j'th k-nearest neighbour
                   for k in range(1, knn_k)]] # over k-nearest neighbours

        rho_knn.sort(key=lambda x: -x[0])  # sort by density

        if rho[i] > rho_knn[0][0]:  # at hilltop? return new label
            print("  new label", next_label)
            label[i] = next_label
            next_label += 1  # create new label  
        else: #  not at hilltop? climb up
            label[i] = climb(rho_knn[0][1], i)

        return label[i]  # return label


def cluster(input_file):
    global data, idx, knn_k, dmat, rho, label, next_label
    idx = range(0, len(data))  # data indices
    label, next_label = [-1 for i in idx], 0  # first label will be 0
    
    dmat, pkl_f = None, input_file + '_dmat.p'
    if os.path.exists(pkl_f):
        print("restoring dmat from pickle file..")
        dmat = pickle.load(open(pkl_f, 'rb'))
    else:
        print("1. sorted distance matrix..")  # memoize?
        dmat = parfor(dmat_row, idx)
        pickle.dump(dmat, open(pkl_f, 'wb'))

    print("2. density estimation..")
    rho()  # density estimation
    print("rho", rho)
    print("3. recursive hillclimbing..")
    for i in idx:
        climb(i)


from read_csv import read_csv, write_output
data, class_label = read_csv(input_file)

if scale_data:
    # scale data to [0, 1]
    min_x, max_x = copy.deepcopy(data[0]), copy.deepcopy(data[0])
    for p in data:
        for k in range(0, len(data[0])):
            min_x[k] = p[k] if p[k] < min_x[k] else min_x[k]
            max_x[k] = p[k] if p[k] > max_x[k] else max_x[k]

    for i in range(0, len(data)):
        for k in range(0, len(data[0])):
            data[i][k] -= min_x[k]
            denom = (max_x[k] - min_x[k])
            if denom != 0.:
                data[i][k] /= denom

print("points", data)  # print out points just in case

# if not specified, set knn_k to be equal to 
if knn_k is None:
    knn_k = math.ceil(math.sqrt(len(data)))
    print("knn_k", knn_k)

cluster(input_file)

print('label', label)
print('class_label', class_label)
print('n_labels', next_label)

from evaluate import class_match, accuracy, consistency

mapping = None
if class_label is not None:
    mapping, count = class_match(label, class_label)
    print(mapping)

    print(accuracy(label, class_label, mapping))

    c = consistency(label, class_label, mapping, count)

    table_filename = input_file + '_table.html'
    open(table_filename, "wb").write(c.encode())

    a = os.system('firefox ' + table_filename)

# can still write output labels, even if no "reference" class data
output_file = input_file + '_output.csv'
print(rho)
write_output(input_file, output_file, label, mapping, rho)

# maybe do later?
# put field names on the three axes (in the 3d plot)
# convert binary class maps (colored with values) to PNG
