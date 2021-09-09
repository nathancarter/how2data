---
author: Nathan Carter (ncarter@bentley.edu)
---

When applying this technique, you would have a series of data values for which
you needed to compute a confidence interval for the mean.  But in order to
provide code that runs independently, we create some fake data below.  When
using this code, replace our fake data with your real data.

```R
alpha <- 0.05       # replace with your chosen alpha (here, a 95% confidence level)
data <- c( 435,542,435,4,54,43,5,43,543,5,432,43,36,7,876,65,5 ) # fake

# If you need the two values stored in variables for later use, do:
answer <- t.test( data, conf.level=alpha )
lower_bound <- answer$conf.int[1]
upper_bound <- answer$conf.int[2]

# If you just need to see the results in a report, do this alone:
t.test( data, conf.level=alpha )
```
