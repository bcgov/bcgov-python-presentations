# read csv file with header: for 3-d float data would expect:

# 0, 1, 2, class
# 0, 1, 2

# optional last row labelled "class" is "truth" data
# --> language use change: let's call this "reference" data

# this file also includes method to write output file
from util import err

def read_csv(file_name):
    global data, idx, class_label
    data, class_label, lines = [], None, open(file_name).readlines()
    idx = range(0, len(lines) - 1)  # -1 for header row
    w = [x.strip() for x in lines[0].strip().split(',')]

    # process header row
    for i in range(0, len(w)):
        if w[i] != str(i):
            if w[i] == 'class':
                class_label = []
            else:
                err("expected w[i] = str(i)")

    # process data
    for i in range(1, len(lines)):
        w = [x.strip() for x in lines[i].strip().split(',')]
        if class_label is not None:
            class_label.append(w[-1])  # class label is last elem
            data.append([float(w[i]) for i in range(0, len(w) -1)])
        else:  # no class label
            data.append([float(w[i]) for i in range(0, len(w))])

    return data, class_label


def write_output(input_file, output_file, label, mapping = None, rho = None):
    print("rho", rho)
    lines = [x.strip() for x in open(input_file).readlines()]
    lines[0] = lines[0].strip() + ',label'
    if mapping is not None:
        lines[0] += ',assigned'
    if rho is not None:
        lines[0] += ',rho'
    for i in range(1, len(lines)):
        j = i - 1
        lines[i] += ',' + str(label[j])
        if mapping is not None:
            lines[i] += (',' + str(mapping[label[j]]))
        if rho is not None:
            lines[i] += (',' + str(rho[j]))
    open(output_file, 'wb').write(('\n'.join(lines)).encode())
