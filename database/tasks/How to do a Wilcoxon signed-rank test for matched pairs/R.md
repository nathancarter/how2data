---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

The method we will use is equivalent to subtracting the two samples and then
performing the signed-rank test.  See how to do a Wilcoxon signed-rank test to
compare the two methods.

We're going to use fake data for illustrative purposes,
but you can replace our fake data with your real data.

```R
# Replace sample1 and sample2 with your data
sample1 <- c(156, 133, 90, 176, 119, 120, 40, 52, 167, 80)
sample2 <- c(45, 36, 78, 54, 12, 25, 39, 48, 52, 70)
```

We choose a value, $0 \le \alpha \le 1$, as the Type I Error Rate. We'll let $\alpha$ be 0.05.

### Two-tailed test

To test the null hypothesis $H_0: m_D = 0$, we use a two-tailed test:

```R
wilcox.test(sample1, sample2, alternative = "two.sided", mu = 0, paired = TRUE)
```

Our p-value, 0.00195, is less than $\alpha=0.05$, so we have sufficient evidence
to reject the null hypothesis. The median difference is significantly different
from zero.

### Right-tailed test

To test the null hypothesis $H_0: m_D \le 0$, we use a right-tailed test:

```R
wilcox.test(sample1, sample2, alternative = "greater", mu = 0, paired = TRUE)
```

Our p-value, 0.0009766, is less than $\alpha=0.05$, so we have sufficient evidence
to reject the null hypothesis. The median difference is significantly greater
than zero.

### Left-tailed test

To test the null hypothesis $H_0: m_D \ge 0$, we use a left-tailed test:

```R
wilcox.test(sample1, sample2, alternative = "less", mu = 0, paired = TRUE)
```

Our p-value, 1.0, is greater than $\alpha$, so we do not have sufficient
evidence to reject the null hypothesis. We should continue to assume that the
mean difference may be less than (or equal to) zero.

NOTE: If there are ties in the data and there are fewer than 50 observations in
each sample, then R will compute a $p$-value using the normal approximation, and
there will be an error message indicating that the exact $p$-value cannot be
calculated.
