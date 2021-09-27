---
author: Nathan Carter (ncarter@bentley.edu)
---

This is a two-sided test with the null hypothesis $H_0:\mu=\bar x$.
We choose a value $0\leq\alpha\leq1$ as the probability of a Type I error
(false positive, finding we should reject $H_0$ when it's actually true).

```python
from scipy import stats

# Replace these first three lines with the values from your situation.
alpha = 0.05
pop_mean = 10
sample = [ 9, 12, 14, 8, 13 ]

# Run a one-sample t-test and print out alpha, the p value,
# and whether the comparison says to reject the null hypothesis.
t_statistic, p_value = stats.ttest_1samp( sample, pop_mean )
reject_H0 = p_value < alpha
alpha, p_value, reject_H0
```

In this case, the sample does not give us enough information to reject
the null hypothesis.  We would continue to assume that the sample is like
the population, $\mu=\bar x$.
