# Simple character recognition
Based on Earth-mover type distance.

1) Flood-fill segmentation
* most-prevalent color assumed to be "background" to be ignored
* characters to be classified are assumed to be of uniform color

2) Wasserstein "earth-mover" (inspired) distance
* simple nearest-centroid "supervised" classification, in the sense that the truth data are the "centroids" with respect to the "earth-mover" distance
* some robustness to noise or transformation offered, relative to truth data

<img src="fig/table.png" width="444px">

# How to run
To generate the truth and test data:

```
python3 render.py
```

To perform flood-fill segmentation on truth and test:

```
python3 segment.py
```

To make a prediction on the test data:

```
python3 predict.py
```


