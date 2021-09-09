---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We're going to use some fake data here to illustrate how to make the confidence
interval. Replace our fake data with your actual data if you use this code.

```R
sample.1 <- c(15, 10, 7, 22, 17, 14)
sample.2 <- c(9, 1, 11, 13, 3, 6)
```

In the example below, we specify `var.equal = FALSE` to indicate that we cannot
assume that the variances are equal.  If you know them to be equal in your situation,
replace `FALSE` with `TRUE`.

```R
alpha <- 0.05       # replace with your chosen alpha (here, a 95% confidence level)
conf.interval <- t.test(sample.1, sample.2, var.equal = FALSE, conf.level = 1-alpha)
# If you need the upper and lower bounds later, store them in variables like this:
lower.bound <- conf.interval$conf.int[1]
upper.bound <- conf.interval$conf.int[2]
# Print out the lower and upper bounds
lower.bound
upper.bound
```

Our 95% confidence interval for the true difference between these population means
is $[0.5852, 13.4147]$.

You can also see the test statistic and $p$-value by inspecting the result of the
`t.test` function we ran above.

```R
conf.interval
```
