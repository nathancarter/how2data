---
author: Nathan Carter (ncarter@bentley.edu)
---

When applying this technique, you would have a series of data values for which
you needed to compute a confidence interval for the mean.  But in order to
provide code that runs independently, we create some fake data below.  When
using this code, replace our fake data with your real data.

```julia
alpha = 0.05       # replace with your chosen alpha (here, a 95% confidence level)
data = [ 435,542,435,4,54,43,5,43,543,5,432,43,36,7,876,65,5 ] # fake

# Compute the confidence interval:
using HypothesisTests
confint( OneSampleTTest( data ), level=1-alpha, tail=:both )
```

*Note:* The solution above assumes that the population is normally distributed,
which is a common assumption in introductory statistics courses,
but we have not verified that assumption here.
