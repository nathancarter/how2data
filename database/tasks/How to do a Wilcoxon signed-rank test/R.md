---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We're going to use fake data for illustrative purposes,
but you can replace our fake data with your real data.
Say our sample, $x_1, x_2, x_3, \ldots x_k$, has median $m$.

```R
# Replace the next line with your data
sample <- c(19, 4, 23, 16, 1, 8, 30, 25, 13)
```

We choose a value, $0 \le \alpha \le 1$, as the Type I Error Rate. We'll let $\alpha$ be 0.05.
In the examples below, we will be comparing the median $m$ to a hypothesized value of
$a=10$, but you can use any value for $a$.

### Two-tailed test

To test the null hypothesis $H_0: m=a$, we use a two-tailed test:

```R
a <- 10
wilcox.test(sample, mu = a, alternative = "two.sided")
```

Our p-value, 0.1544, is greater than $\alpha=0.05$, so we do not have
sufficient evidence to reject the null hypothesis. We may continue to assume
the population median is equal to 10.

### Right-tailed test

To test the null hypothesis $H_0: m\ge a$, we use a right-tailed test:

```R
wilcox.test(sample, mu = a, alternative = "less")
```

Our p-value, 0.9386, is greater than $\alpha=0.05$, so we do not have
sufficient evidence to reject the null hypothesis. We may continue to assume
the population median is less than (or equal to) 10.

### Left-tailed test

To test the null hypothesis $H_0: m\le a$, we use a left-tailed test:

```R
wilcox.test(sample, mu = a, alternative = "greater")
```

Our p-value, 0.0772, is greater than $\alpha$, so we do not have sufficient
evidence to reject the null hypothesis. We may continue to assume the population
median is greater than (or equal to) 10.

NOTE: If there are ties in the data and there are fewer than 50 observations in each sample, then R will compute a $p$-value using the normal approximation, and there will be an error message indicating that the exact $p$-value cannot be calculated.
