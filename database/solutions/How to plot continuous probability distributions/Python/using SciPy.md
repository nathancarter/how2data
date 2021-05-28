---
author: Nathan Carter (ncarter@bentley.edu)
---

You can import many different random variables from SciPy's `stats` module.
The full list of them is online [here](https://docs.scipy.org/doc/scipy/reference/stats.html#discrete-distributions).

The challenge with plotting a random variable is knowing the appropriate
sample space, because some random variables have sample spaces of infinite
width, which cannot be plotted.

But we can just ask SciPy to show us the central 99.98% of a continuous
distribution, which is almost always indistinguishable
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
