---
author: Nathan Carter (ncarter@bentley.edu)
---

When applying this technique, you would have a series of data values for which
you needed to compute a confidence interval for the mean.  But in order to
provide code that runs independently, we create some fake data below.  When
using this code, replace our fake data with your real data.

We include the population standard deviation below, assuming it is known.
See the notes at the end for what to do if you do not know the population
standard deviation in your situation.

```R
alpha <- 0.05       # replace with your chosen alpha (here, a 95% confidence level)
pop.std <- 250      # replace with your population standard devation, if known
data <- c( 435,542,435,4,54,43,5,43,543,5,432,43,36,7,876,65,5 ) # fake

# Compute the sample mean, as an estimate for the population mean.
sample.mean <- mean( data )

# The margin of error then has the following formula.
z.score <- qnorm( alpha / 2, lower.tail=FALSE )
moe <- pop.std * z.score / sqrt( length( data ) )

# The confidence interval is centered on the mean with moe as its radius:
c( sample.mean - moe, sample.mean + moe )
```

Notes:

 1. If you do not have the population standard deviation, but your sample is
    large enough (typically at least 30), you can approximate the population
    standard deviation with the sample standard deviation, using the code
    `pop.std <- sd( data )`.  If your sample is not that large, then
    consider using a different technique instead; see
    how to compute a confidence interval for a population mean.
 2. The solution above assumes that the population is normally distributed,
    which is a common assumption in introductory statistics courses, but we
    have not verified that assumption here.
