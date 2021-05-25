# Simple character recognition
* based on Earth-mover type distance

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


