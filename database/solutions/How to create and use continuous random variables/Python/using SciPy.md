---
author: Nathan Carter (ncarter@bentley.edu)
---

You can import many different random variables from SciPy's `stats` module.
The full list of them is online [here](https://docs.scipy.org/doc/scipy/reference/stats.html#discrete-distributions).
The examples below use the normal and uniform distributions as examples.

You can **create random variables** as follows.

```python
from scipy import stats

# A normal random variable with mean 10 and standard deviation 5
X1 = stats.norm( loc=10, scale=5 )
# A uniform random variable on the interval from 50 to 60
# (loc is the starting point and scale is the size of the sample space,
# which in this case is 60-50=10)
X2 = stats.uniform( loc=50, scale=10 )
```

You can **compute the probability** of any interval in the sample space.
Each random variable comes with a cumulative density function (CDF), and
you can use subtraction to compute the probability on an interval $[a,b]$.

```python
X1.cdf( 13 ) - X1.cdf( 12 )   # probability of being in the interval [12,13]
```

You can **generate random values.**  The `rvs` function is short for "random
values."

```python
X2.rvs( 10 )  # generates 10 random values from X2
```

You can **compute statistics** about the distributions you create.  Here,
`var` is short for variance, and `std` for standard deviation.

```python
X1.mean(), X1.var(), X1.std()
```

You can **plot the distribution** of a continuous random variable.

Here we plot the middle 99.98% of the distribution, but you can adjust
the numbers to plot less or more.  (We cannot plot all of the distribution,
because some distributions have sample spaces of infinite width.)

```python
import matplotlib.pyplot as plt
import numpy as np
xmin = X1.ppf( 0.0001 )   # find lowest x value we will use in our plot
xmax = X1.ppf( 0.9999 )   # find highest x value we will use in our plot
xs = np.linspace( xmin, xmax, 100 )  # create 100 x values in that range
plt.plot( xs, X1.pdf( xs ) )         # plot the curve
plt.show()
```
