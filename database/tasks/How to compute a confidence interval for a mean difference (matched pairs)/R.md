---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

This example computes a 95% confidence interval,
but you can choose a different level by choosing a different value for $\alpha$.

```R
alpha = 0.05
```

We have two samples of data, $x_1, x_2, x_3, \ldots, x_k$ and $x'_1, x'_2, x'_3, \ldots, x'_k$.
We're going to use some fake data below just as an example; replace it with your real data.

```R
sample.1 <- c(15, 10, 7, 22, 17, 14)
sample.2 <- c(9, 1, 11, 13, 3, 6)
```

The shortest way to create the confidence interval is with R's `t.test()` function.
It's just one line of code.

```R
t.test(sample.1, sample.2, paired = TRUE, conf.level = 1-alpha)
```

If you need the lower and upper bounds later, you can save them as variables as follows.

```R
conf.interval <- t.test(sample.1, sample.2, paired = TRUE, conf.level = 1-alpha)
lower.bound <- conf.interval$conf.int[1]
upper.bound <- conf.interval$conf.int[2]
```

It's also possible to do the computation manually, using the code below.

```R
diff.samples <- sample.1 - sample.2                # differences between the samples
n = length(sample.1)                               # number of observations per sample
diff.mean <- mean(diff.samples)                    # mean of the differences
diff.variance <- var( diff.samples )               # variance of the differences
critical.val <- qt(p = alpha/2, df = n - 1,
    lower.tail=FALSE)                              # critical value
radius <- critical.val*sqrt(diff.variance)/sqrt(n) # radius of confidence interval
c( diff.mean - radius, diff.mean + radius )        # confidence interval
```

Either method gives the same result. Our 95% confidence interval is $[0.70338, 13.2966]$.
