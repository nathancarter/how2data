---
author: Nathan Carter (ncarter@bentley.edu)
---

You can import many different random variables from SciPy's `stats` module.
The full list of them is online [here](https://docs.scipy.org/doc/scipy/reference/stats.html#discrete-distributions).
The examples below use the Bernoulli and binomial distributions as examples.

You can **create random variables** as follows.

```python
from scipy import stats

# A Bernoulli random variable with p=0.25 probability of success
X1 = stats.bernoulli( 0.25 )
# A binomial random variable with 10 trials
# and p=0.5 probability of success on each
X2 = stats.binom( 10, 0.5 )
```

You can **compute the probability** of any given outcome.  The `pmf` function
stands for "probability mass function," which assigns probabilities to
outcomes.

```python
X2.pmf( 3 )   # probability of exactly 3 successes in the 10 trials
```

You can **generate random values.**  The `rvs` function is short for "random
values."

```python
X1.rvs( 10 )  # generates 10 random values from X1
```

You can **compute statistics** about the distributions you create.  Here,
`var` is short for variance, and `std` for standard deviation.

```python
X1.mean(), X1.var(), X1.std()
```

You can **plot the distribution** of a discrete random variable.

Note that you must supply the sample space, because it is not always
possible to compute it; some sample spaces are infinite, and you must
choose which subset of the infinite sample space ($x$ axis) you want to view.

```python
import matplotlib.pyplot as plt
import numpy as np
xs = np.arange( 0, 11 )   # choose the sample space...here, it's 0,1,2...,10
ys = X2.pmf( xs )         # compute the shape of the distribution
plt.plot( xs, ys, 'o' )   # plot circles...
plt.vlines( xs, 0, ys )   # ...and lines
plt.ylim( bottom=0 )      # ensure sensible bottom border
plt.show()
```
