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

To create a box-and-whisker plot, sometimes called just a box plot requires just one line of code, plus one to show the plot.

```python
plt.boxplot( patient_height )
plt.show()
```

You can show more than one variable's box plot side-by-side by forming a list of the data.

```python
plt.boxplot( [ patient_height, patient_weight ] )
plt.show()
```


