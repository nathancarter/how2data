---
author:
 - Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
 - Nathan Carter (ncarter@bentley.edu)
---

We will use the following fake data, but you can insert your actual data in its place.
We have a sample of just 5 values and an assumed population standard deviation of 3.

```R
sample <- c(31, 44, 28, 25, 40)  # sample data
pop.std <- 3                     # population standard deviation
```

We also choose a value $0 \le \alpha \le 1$ as our Type I error rate.
We'll let $\alpha$ be 0.05 here, but you can change that in the code below.

### Two-tailed test

In a two-tailed test, we compare the unknown population mean to a hypothesized
value $m$ using the null hypothesis $H_0: \mu=m$.
Here we'll use $m=30$, but you can replace that value in the code
below with the hypothesis relevant for your situation.

```R
m <- 30                                           # hypothesized mean
n <- length(sample)                               # number of observations
xbar <- mean(sample)                              # sample mean
test.stat <- (xbar - m) / (pop.std/sqrt(n))       # test statistic
2*pnorm(abs(test.stat), 0, 1, lower.tail=FALSE)   # two-tailed p-value
```

The $p$-value, 0.00729, is less than $\alpha$, so we have evidence to reject the
null hypothesis and conclude that the actual population mean $\mu$ is significantly
different from the hypothesized value of $m=30$.

### Right-tailed test

In a right-tailed hypothesis test, the null hypothesis is that the population mean
is greater than or equal to a chosen value, $H_0: \mu \ge m$.

Most of the code below is the same as above, but we repeat it to make it easy to
copy and paste.  Only the computation of the $p$-value changes.

```R
m <- 30                                      # hypothesized mean
n <- length(sample)                          # number of observations
xbar <- mean(sample)                         # sample mean
test.stat <- (xbar - m) / (pop.std/sqrt(n))  # test statistic
pnorm(test.stat, 0, 1, lower.tail=FALSE)     # right-tailed p-value
```

The $p$-value, 0.003645, is less than $\alpha$, so we have evidence to reject the
null hypothesis and conclude that the actual population mean $\mu$ is significantly
less than the hypothesized value of $m=30$.

### Left-tailed test

In a left-tailed hypothesis test, the null hypothesis is that the population mean
is less than or equal to a chosen value, $H_0: \mu \le m$.

Most of the code below is the same as above, but we repeat it to make it easy to
copy and paste.  Only the computation of the $p$-value changes.

```R
m <- 30                                      # hypothesized mean
n <- length(sample)                          # number of observations
xbar <- mean(sample)                         # sample mean
test.stat <- (xbar - m) / (pop.std/sqrt(n))  # test statistic
pnorm(test.stat, 0, 1, lower.tail=TRUE)      # left-tailed p-value
```

The $p$-value, 0.99635, is greater than $\alpha$, so wwe do not have sufficient
evidence to conclude that $\mu>m$ and should continue to accept the null hypothesis,
that $\mu\le m$.
