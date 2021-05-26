'''flood fill segmentation'''
def flood(img, i, j, my_label=None, my_color=None):
    if i >= img.rows or j >= img.cols or i < 0 or j < 0:
        return  # out of bounds
    ix = i * img.cols + j  # linear index of (i, j)

    if img.labels[ix] > 0:
        return  # stop: already labelled

    c_s = str(img.rgb[ix])
    if c_s == img.max_color:
        return  # stop: ignore background "background subtraction"
    if my_color and my_color != c_s:
        return  # stop: different colour than at invocation chain start

    if my_label:
        img.labels[ix] = my_label
    else:
        img.labels[ix] = img.next_label
        img.next_label += 1

    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if not (di == 0 and dj == 0):
                flood(img, i + di, j + dj, img.labels[ix], c_s)


