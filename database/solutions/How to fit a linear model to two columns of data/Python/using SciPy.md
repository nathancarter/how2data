---
author: Nathan Carter (ncarter@bentley.edu)
---

This solution uses a pandas DataFrame of fake example data.
When using this code, replace our fake data with your real data.

Although the solution below uses plain Python lists of data, it also works if
the data are stored in NumPy arrays or pandas Series.

```python
# Here is the fake data you should replace with your real data.
xs = [ 393, 453, 553, 679, 729, 748, 817 ]
ys = [  24,  25,  27,  36,  55,  68,  84 ]

# We will use SciPy to build the model
import scipy.stats as stats

# If you need the model coefficients stored in variables for later use, do:
model = stats.linregress( xs, ys )
beta0 = model.intercept
beta1 = model.slope

# If you just need to see the coefficients (and some other related data),
# do this alone:
stats.linregress( xs, ys )
```
