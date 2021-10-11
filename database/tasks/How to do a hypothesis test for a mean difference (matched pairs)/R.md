---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We choose a value, $0 \le \alpha \le 1$, as the Type I Error rate, and in this case
we will set it to be 0.05.

We're going to use fake fata here, but you can replace our fake data with your real data below.
Because the data are matched pairs, the samples must be the same size.

```R
# Replace the following example data with your real data
sample.1 <- c(15, 10,  7, 22, 17, 14)
sample.2 <- c( 9,  1, 11, 13,  3,  6)
```

### Two-tailed test

In a two-sided hypothesis test, the null hypothesis states that the mean
difference is equal to 0 (or some other hypothesized value), $H_0: \mu_D = 0$.

```R
alpha = 0.05
t.test(sample.1, sample.2, alternative = "two.sided",
       mu = 0, paired = TRUE, conf.level = 1-alpha)
```

Our $p$-value, 0.0355, appears in the third line of the output.  It is smaller
than $\alpha$, so we have sufficient evidence to reject the null hypothesis and
conclude that the mean difference between the two samples is significantly
different from zero. 

If we want instead to test whether it is some other value $d\neq0$, then just
use that value as the `mu` parameter to the `t.test` function instead of zero.

### Right-tailed test

If instead we want to test whether the mean difference is less than or equal to
zero, $H_0: \mu_D\le0$, we can use a right-tailed test, as follows.

```R
t.test(sample.1, sample.2, alternative = "greater",
       mu = 0, paired = TRUE, conf.level = 1-alpha)
```

Our $p$-value, 0.01775, is smaller than $\alpha$, so we have sufficient evidence
to reject the null hypothesis and conclude that the mean difference between the
two samples is significantly greater than zero.

Again, you can use another value $d\neq0$ in place of `mu = 0` in the code.

### Left-tailed test

If instead we want to test whether the mean difference is greater than or equal to
zero, $H_0: \mu_D\ge0$, we can use a right-tailed test, as follows.

```R
t.test(sample.1, sample.2, alternative = "less",
       mu = 0, paired = TRUE, conf.level = 1-alpha)
```

Our $p$-value, 0.9822, is larger than $\alpha$, so we do not have sufficient evidence
to reject the null hypothesis; we must continue to assume that the mean difference
between the two samples is greater than or equal to zero.

Again, you can use another value $d\neq0$ in place of `mu = 0` in the code.
