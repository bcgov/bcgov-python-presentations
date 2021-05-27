# Simple character recognition
## slides
* [please click here for slides](https://github.com/bcgov/bcgov-python-presentations/blob/master/presentations/20210526_simple_character_recognition/slides/20210526_arithmancy.pdf)
## details
Based on Earth-mover type distance.

1) Flood-fill segmentation
* most-prevalent color assumed to be "background" to be ignored
* characters to be classified are assumed to be of uniform color

2) Wasserstein "earth-mover" (inspired) distance
* simple nearest-centroid "supervised" classification, in the sense that the truth data are the "centroids" with respect to the "earth-mover" distance
* some robustness to noise or transformation offered, relative to truth data

<img src="fig/table.png" width="444px">

## how to run
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


## potential improvements
* Stopping after specified threshold (thanks Ken!)
* incremental sampling approach to see how many points are required to be sampled before reaching a threshold
* look at effects of distortions on characters! 

# References 
Read these to figure out how to do a Wasserstein distance properly!
* [Models for Particle Image Velocimetry: Optimal Transportation and Navier-Stokes Equations](https://dspace.library.uvic.ca/bitstream/handle/1828/7041/SaumierDemers_LouisPhilippe_PhD_2015.pdf) PhD Thesis, L-P Saumier (2016)
* [An efficient numerical algorithm for the L2 optimal transport problem with applications to image processing](http://dspace.library.uvic.ca/bitstream/handle/1828/3157/LPSaumierMScThesis.pdf) M.Sc. Thesis, L-P Saumier (2010)


