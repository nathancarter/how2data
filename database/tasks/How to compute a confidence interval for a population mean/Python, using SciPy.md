---
author: Nathan Carter (ncarter@bentley.edu)
---

This solution uses a 95% confidence level, but you can change that in the
first line of code, by specifing a different `alpha`.

When applying this technique, you would have a series of data values for which
you needed to compute a confidence interval for the mean.  But in order to
provide code that runs independently, we create some fake data below.  When
using this code, replace our fake data with your real data.

```python
alpha = 0.05       # replace with your chosen alpha (here, a 95% confidence level)
data = [ 435,542,435,4,54,43,5,43,543,5,432,43,36,7,876,65,5 ] # fake

# We will use NumPy and SciPy to compute some of the statistics below.
import numpy as np
import scipy.stats as stats

# Compute the sample mean, as an estimate for the population mean.
sample_mean = np.mean( data )

# Compute the Standard Error for the sample Mean (SEM).
sem = stats.sem( data )

# The margin of error then has the following formula.
moe = sem * stats.t.ppf( 1 - alpha / 2, len( data ) - 1 )

# The confidence interval is centered on the mean with moe as its radius:
( sample_mean - moe, sample_mean + moe )
```

*Note:* The solution above assumes that the population is normally distributed,
which is a common assumption in introductory statistics courses,
but we have not verified that assumption here.
