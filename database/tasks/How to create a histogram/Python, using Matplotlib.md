---
author: Nathan Carter (ncarter@bentley.edu)
---

We will create some random data using NumPy, but that's just for demonstration purposes.  You can apply the answer below to any data, even if it's stored just in plain Python lists.

```python
import numpy as np
data = np.random.normal( size=1000 )
```

The conventional way to import matplotlib in Python is as follows.

```python
import matplotlib.pyplot as plt
```

To create a histogram with 10 bins (the default):

```python
plt.hist( data )  # or plt.hist( bins=20 ), or any number
plt.show()
```

The $y$ axis in a histogram is frequency, or number of occurrences.  You can change it to probabilities instead.

```python
plt.hist( data, density=True )
plt.show()
```

You can also choose your own bin boundaries.

```python
plt.hist( data, bins=range(-10,10,1) )
plt.show()
```

