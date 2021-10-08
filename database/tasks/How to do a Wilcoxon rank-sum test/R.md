---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We're going to use fake data for illustrative purposes,
but you can replace our fake data with your real data.
Say our first sample, $x_1, x_2, x_3, \ldots x_k$, has median $m_1$,
and our second sample, $x'_1, x'_2, x'_3, \ldots x'_k$, has median $m_2$.

```R
# Replace sample1 and sample2 with your data
sample1 <- c(56, 31, 190, 176, 119, 15, 140, 152, 167, 180)
sample2 <- c(45, 36, 78, 54, 12, 25, 39, 48, 52, 70)
```

We choose a value, $0 \le \alpha \le 1$, as the Type I Error Rate. We'll let $\alpha$ be 0.05.

### Two-tailed test

To test the null hypothesis $H_0: m_1 - m_2 = 0$, that is, $m_1=m_2$, we use a two-tailed test:

```R
wilcox.test(sample1, sample2, alternative = "two.sided", mu = 0, paired = FALSE)
```

Our p-value, 0.01854, is less than $\alpha=0.05$, so we have sufficient evidence
to reject the null hypothesis. The population medians are significantly different
from each other.

### Right-tailed test

To test the null hypothesis $H_0: m_1 - m_2 \le 0$, that is, $m_1\le m_2$, we use a right-tailed test:

```R
wilcox.test(sample1, sample2, alternative = "greater", mu = 0, paired = FALSE)
```

Our p-value, 0.009272, is less than $\alpha=0.05$, so we have sufficient evidence
to reject the null hypothesis. The first population medians is significantly greater
second.

### Left-tailed test

To test the null hypothesis $H_0: m_1 - m_2 \ge 0$, that is, $m_1\ge m_2$, we use a left-tailed test:

```R
wilcox.test(sample1, sample2, alternative = "less", mu = 0, paired = FALSE)
```

Our p-value, 0.9927, is greater than $\alpha$, so we do not have sufficient
evidence to reject the null hypothesis. The first population median is not
significantly smaller than the second population median.

NOTE: If there are ties in the data and there are fewer than 50 observations in each sample, then R will compute a $p$-value using the normal approximation, and there will be an error message indicating that the exact $p$-value cannot be calculated.
