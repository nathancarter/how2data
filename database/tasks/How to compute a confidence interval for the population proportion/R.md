---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We're going to use some fake data here for illustrative purposes,
but you can replace our fake data with your real data in the code below.

```R
# Replace the next two lines of code with your real data
sample_size = 30
sample_proportion = 0.39

# Find the margin of error
alpha <- 0.05       # replace with your chosen alpha (here, a 95% confidence level)
moe <- qnorm(1-alpha/2, 0, 1) * sqrt(sample_proportion*(1-sample_proportion)/sample_size)

# Find the confidence interval
upper_bound <- sample_proportion + moe
lower_bound <- sample_proportion - moe
lower_bound
upper_bound
```

Our 95% confidence interval is $[0.2155, 0.5645]$.
