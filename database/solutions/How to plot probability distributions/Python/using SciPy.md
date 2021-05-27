---
author: Nathan Carter (ncarter@bentley.edu)
---

You can import many different random variables from SciPy's `stats` module.
The full list of them is online [here](https://docs.scipy.org/doc/scipy/reference/stats.html#discrete-distributions).

The challenge with plotting a random variable is knowing the appropriate
sample space, because some random variables have sample spaces of infinite
width, which cannot be plotted.  So there are two options.

For a **discrete distribution,** you often want to specify the range.

The example below uses a geometric distribution, whose sample space is
$\{1,2,3,\ldots\}$.  We specify that we just want to use $x$ values
in the set $\{1,2,\ldots,10\}$.  (In some software, the geometric
distribution's sample space begins at 0, but not in SciPy.)

We style the plot below so that it is clear the sample space is discrete.

```python
from scipy import stats
X = stats.geom( 0.5 )     # use a geometric distribution with p=0.5

import numpy as np
xs = np.arange( 1, 11 )   # specify the range to be 1,2,3,...,10

import matplotlib.pyplot as plt
ys = X.pmf( xs )          # compute the shape of the distribution
plt.plot( xs, ys, 'o' )   # plot circles...
plt.vlines( xs, 0, ys )   # ...and lines
plt.ylim( bottom=0 )      # ensure sensible bottom border
plt.show()
```

For a **continuous distribution,** you can just ask SciPy to show you the
central 99.98% of the distribution, which is almost always indistinguishable
to the human eye from the entire distribution.

We style the plot below so that it is clear the sample space is continuous.

```python
from scipy import stats
X = stats.norm( 10, 5 )      # use a normal distribution with μ=10 and σ=5

xmin = X.ppf( 0.0001 )       # compute min x as the 0.0001 quantile
xmax = X.ppf( 0.9999 )       # compute max x as the 0.9999 quantile
import numpy as np
xs = np.linspace( xmin, xmax, 100 )  # create 100 x values in that range

import matplotlib.pyplot as plt
plt.plot( xs, X.pdf( xs ) )  # plot the shape of the distribution
plt.show()
```
