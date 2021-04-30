# heuristic to match "truth" / reference labels, with unsupervised-derived labels
# also, includes accuracy and confusion matrix calculation

def class_match(label, class_label):  # submode class-matching
    # simple algorithm to assign class ("truth") label to unsupervised label
    
    count, idx = {}, range(0, len(label))
    for i in idx:  # data-driven matching, by iterating the data
        lab, class_lab = label[i], class_label[i]
        
        if lab not in count:
            count[lab] = {}

        if class_lab not in count[lab]:
            count[lab][class_lab] = 0
        count[lab][class_lab] += 1

    mapping = {}
    for i in count:
        print(i, count[i])
        # for label on data[i], find "truth" / reference label, with highest count for this
        ref = list(count[i].keys())
        max_r, max_c = ref[0], count[i][ref[0]]

        if len(ref) > 1:
            for j in range(1, len(ref)):
                print(" count[i][ref[j]]",  count[i][ref[j]] , "max_r", max_r)
                if count[i][ref[j]] > max_c:
                    max_r, max_c = ref[j], count[i][ref[j]]
        mapping[i] = max_r # assign "truth" / reference class label, to unsupervised label i
    return mapping, count

# mapping = class_match(label, class_label)
# print(mapping)


def accuracy(label, class_label, mapping):
    result, n, agree = [mapping[x] for x in label], len(label), 0

    # count labels that agree
    for i in range(0, n):
        if result[i] == class_label[i]:
            agree += 1

    return 100. * float(agree) / float(n)


def consistency(label, class_label, mapping, count):
    predictions = set(label)
    reference = set(class_label)

    print("predictions", predictions)
    print("references", reference)

    s = ""
    s += '<html>\n'
    s += '<table border="1">\n'
    s += '<tr><th>reference(→)<br>predicted(↓),</th>'
    for a in predictions:
        s += ('<th>' + mapping[a] + '</th>')
    s += '</tr>\n'

    for p in predictions:
        s += '<tr><td><b>'
        s += str(mapping[p])
        s += '</b></td>'
        for a in predictions:
            a = mapping[a]
            s += '<td>'
            try:
                s += str(count[p][a])
            except:
                s += str(0)
            s += '</td>'
        s += '\n'
    s += '</table>\n'
    s += '</html>\n'
    return s
