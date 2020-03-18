# 3d viewer for output files from kgc.py
# if you ran:
#    kgc.py input_file.csv
# the output file will be:
#    input_file.csv_output.csv

# colour switching: if you press 0, followed by return, this changes to the default class-colouring
# if you press 1, followed by return, this switches to visualizing the density estimate
# if you press 2, followed by return, switches to visualizing the density estimate, scaled on
# each class, so that the maximum density for that class, is equal to one

from util import *
points, spheres, labels, rho, lookup = [], [], [], [], {}
if len(args) < 2: err('view.py [input file name: *.csv_output.csv from kgc.py]')

# open the csv file
lines = open(args[1]).readlines()
hdr, n_numeric = lines[0], 0  # csv header, number of fields
w = [x.strip() for x in hdr.strip().split(',')]
print('csv header', w)
for i in range(0, len(w)):
    try: n_numeric = int(w[i]) + 1
    except Exception: break
print("count of number of numeric fields: ", n_numeric)
hdr = w
f_i = {w[i]: i for i in range(0, len(w))}
i_f = {i: w[i] for i in range(0, len(w))}

data = {i: [] for i in range(0, len(w))}
for i in range(1, len(lines)):
    w = lines[i].strip().split(',')
    for j in range(0, len(w)):
        try: w[j] = float(w[j]) if j < n_numeric else int(w[j])
        except Exception: pass
        data[j].append(w[j])
 
# retrieve non-numeric fields: class,label,assigned,rho
my_class, my_label, my_assigned, my_rho = None, None, None, None
try: my_class = data[f_i['class']]
except Exception: pass

try: my_label = data[f_i['label']]
except Exception: pass

try: my_assigned = data[f_i['assigned']]
except Exception: pass

try: my_rho = [float(x) for x in data[f_i['rho']]]
except Exception: pass

mn, mx = my_rho[0], my_rho[0]
for i in range(0, len(my_rho)):
    ri = my_rho[i]
    if ri < mn: mn = ri
    if ri > mx: mx = ri
print("mn", mn, "mx", mx)
try: my_rho = [(my_rho[i] - mn) / (mx - mn) for i in range(0, len(my_rho))]
except Exception: pass
print("my_rho", my_rho)

# find max density, per label
mn_lab, mx_lab = {}, {}
for i in range(0, len(my_rho)):
    r, li = my_rho[i], my_label[i]
    if li not in mn_lab:
        mn_lab[li], mx_lab[li] = r, r
    if r < mn_lab[li]: mn_lab[li] = r
    if r > mx_lab[li]: mx_lab[li] = r

print("labels", my_label)
print('len(labels)', len(my_label))
print('len(lines)', len(lines))
labels = set(my_label) # count the number of unique labels
next_label = len(labels)

# colour scheme for points, by going around the colour wheel!
colours = [color.hsv_to_rgb(vector( i / next_label, 1., 1.)) for i in range(0, next_label)] #  + 1)]
print("colours", colours)

# don't forget to shift the index due to header row offset
for ii in range(1, len(lines)):
    point = [data[j][ii- 1] for j in range(0, n_numeric)]
    points.append(point)
print("len(points)", len(points))  # verify point count

scale_data = True # default: data scaling on
if scale_data: # scale data to [0, 1]
    min_x, max_x = copy.deepcopy(points[0]), copy.deepcopy(points[0])
    for i in range(0, len(points)):
        p = points[i]
        for k in range(0, len(p)):
            min_x[k] = p[k] if p[k] < min_x[k] else min_x[k]
            max_x[k] = p[k] if p[k] > max_x[k] else max_x[k]

    for i in range(0, len(points)):
        for k in range(0, len(p)):
            points[i][k] -= min_x[k]
            denom = (max_x[k] - min_x[k])
            if denom != 0.:
                points[i][k] /= denom


print("npoints", len(points))
for i in range(0, len(points)):
    p = points[i]
    # plot each point in 3d with vpython's "sphere"
    s = sphere(pos=vector(p[0], p[1], p[2]),
                          radius=0.033,
                          color=colours[my_label[i]]) # .cyan))
    spheres.append(s)
    lookup[s] = i  # be able to trace the visual, back to the data!

# interaction part: if you click on a sphere, "centre" the viewer there
lastpick, lastcolor, band_select = None, None, [0, 1, 2]
xyz, txt = [None, None, None], [None, None, None] # xyz axes and labels

def getevent():
    global lastpick, lastcolor, lookup, lines
    pick = scene.mouse.pick
    if pick != None:
        lastpick = pick  # pick.color = vector(1, 1, 1) - pick.color
        centre = copy.deepcopy(pick.pos)  # copy to ensure not write-modifying the value

        # translate "centre" to selected sphere
        for i in range(0, len(spheres)):
            spheres[i].pos -= centre 

        # don't forget to move the axes / labels too!
        for i in range(0, len(xyz)):
            xyz[i].pos -= centre
            txt[i].pos -= centre
        
        # find the index of this sphere, so we can print out the data record:
        i = lookup[pick]
        print("record index i=", i, "data:", lines[i + 1])

key_buf = ''
def key(evt):
    global key_buf, spheres, points, colours, my_label #, knn_k 
    k = evt.key
    if k == '\n':
        try:
            i = int(key_buf)
            if i == 0:
                print("i==0")
                for i in range(0, len(points)):
                    spheres[i].color = colours[my_label[i]]
            if i == 1:
                print("i==1")
                for i in range(0, len(points)):
                    r = my_rho[i]
                    spheres[i].color = vector(r, r, r)
                    # (my_rho[i] * vector(1, 0, 0) + (1.-my_rho[i]) * vector(0, 0, 1))
            if i == 2:
                for i in range(0, len(points)):
                    r = my_rho[i]
                    li = my_label[i]
                    r = r - mn_lab[li]
                    r /= (mx_lab[li] - mn_lab[li])
                    spheres[i].color = vector(r, r, r)
                    # (my_rho[i] * vector(1, 0, 0) + (1.-my_rho[i]) * vector(0, 0, 1))
        except Exception:
            # band selector: change dimensions for 3d display
            if key_buf[0] in ['r', 'g', 'b']:
                try:
                    i = int(key_buf[1:])
                    j = {'r':0, 'g':1, 'b':2}[key_buf[0]]
                    if i >=0 and i < n_numeric: # print("i, j", i, j)
                        band_select[j] = i;
                        print("band_select", band_select)
                        for i in range(0, len(points)):
                            p, bs = points[i], band_select
                            spheres[i].pos = vector(float(p[bs[0]]),
                                                    float(p[bs[1]]),
                                                    float(p[bs[2]]))
                except:
                    pass
            

        key_buf = ''  # print(key_buf)
    else:
        key_buf = key_buf + k # allow user to enter multi-character string

# vpython stuff
scene.bind("mousedown", getevent)
scene.bind('keydown', key)
scene.width, scene.height = 1600, 1600
scene.fullscren = True
autoscale = True
userpan = True # shift + left click  = pan

# axes arrows
xyz = [arrow(pos=vector(0,0,0), axis=vector(1,0,0), shaftwidth=.01, color=.5 * color.red),
       arrow(pos=vector(0,0,0), axis=vector(0,1,0), shaftwidth=.01, color=.5 * color.green),
       arrow(pos=vector(0,0,0), axis=vector(0,0,1), shaftwidth=.01, color=.5 * color.blue)]

# axes labels text
txt = [text(text='x', align='center', color=color.red,   pos=vector(1,0,0), height=0.1),
       text(text='y', align='center', color=color.green, pos=vector(0,1,0), height=0.1),
       text(text='z', align='center', color=color.blue,  pos=vector(0,0,1), height=0.1)]

# should have an option to do higher dimensional (with MDS translating to 3d, or dimension switcher)
