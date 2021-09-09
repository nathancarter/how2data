---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We're going to use some fake data here to illustrate how to make the confidence
interval. Replace our fake data and population variances with your actual data
and population variances if you use this code.

```R
sample.1 <- c(15, 10, 7, 22, 17, 14)
sample.2 <- c(9, 1, 11, 13, 3, 6)
pop1.variance <- 2.3
pop2.variance <- 3
```

We will need the size and mean of each sample.

```R
n.sample1 <- length(sample.1)
n.sample2 <- length(sample.2)
xbar1 <- mean(sample.1)
xbar2 <- mean(sample.2)
```

We can then use that data to create the confidence interval.

```R
# Find the critical value from the normal distribution
alpha <- 0.05       # replace with your chosen alpha (here, a 95% confidence level)
critical.val <- qnorm(p=alpha/2, lower.tail=FALSE)

# Find the lower and upper bounds of the confidence interval
radius <- critical.val*sqrt(pop1.variance/n.sample1 + pop2.variance/n.sample2)
upper.bound <- (xbar1 - xbar2) + radius
lower.bound <- (xbar1 - xbar2) - radius
lower.bound
upper.bound
```

Our 95% confidence interval for the true difference between the population means
is $[5.1579, 8.842]$.
