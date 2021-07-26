---
author: Nathan Carter (ncarter@bentley.edu)
---

We will create some fake data using Python lists, for simplicity.  But everything we show below works also if your data is in columns of a DataFrame, such as `df['age']`.

```python
patient_id     = [   0,   1,   2,   3,   4,   5,   6,   7,   8,   9 ]
patient_height = [  60,  64,  64,  65,  66,  66,  70,  72,  72,  76 ]
patient_weight = [ 141, 182, 169, 204, 138, 198, 180, 175, 244, 196 ]
```

The conventional way to import matplotlib in Python is as follows.

```python
import matplotlib.pyplot as plt
```

Make a line plot by giving the $x$ and $y$​ data values in separate lists (or in this case pandas Series).  This line plot is very jagged just because the data was random.

```python
plt.plot( patient_id, patient_height )         # create plot
plt.show()                                     # display plot
```

You can make a scatterplot as follows.

```python
plt.scatter( patient_height, patient_weight )  # create plot
plt.show()                                     # display plot
```

If your data is already in a pandas DataFrame, there are shortcuts:

~~~python
# Plot all columns:
df.plot()
plt.show()

# Plot all columns in separate subplots:
df.plot( subplots = True )
plt.show()

# Plot one column:
df['column'].plot()
plt.show()

# Plot specific columns:
df.plot( x='col name', y='other col name' )
plt.show()
~~~

