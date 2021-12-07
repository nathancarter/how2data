---
author: Nathan Carter (ncarter@bentley.edu)
---

If we call the mean of the first sample $\bar x_1$ and the mean of the
second sample $\bar x_2$, then this is a two-sided test
with the null hypothesis $H_0: \bar x_1 - \bar x_2 \ge 0$.
We choose a value $0\leq\alpha\leq1$ as the probability of a Type I error
(false positive, finding we should reject $H_0$ when it's actually true).
Let's use $\alpha=0.10$ as an example.

```python
from scipy import stats

# Replace these first three lines with the values from your situation.
sample1 = [ 6, 9, 7, 10, 10, 9 ]
sample2 = [ 12, 14, 10, 17, 9 ]

# Run a one-sample t-test and print out alpha, the p value,
# and whether the comparison says to reject the null hypothesis.
stats.ttest_ind( sample1, sample2, equal_var=False, alternative="less" )
```

The output says that the $p$-value is about $0.0255$, which is less than $\alpha=0.10$.
Therefore the samples give us enough evidence to reject the null hypothesis
at the $\alpha=0.10$ level.  That is, the data suggest that $\bar x_1 < \bar x_2$.

The `equal_var` parameter tells SciPy *not* to assume that the two samples
have equal variances.  If in your case they do, you can omit that parameter,
and it will revert to its default value of `True`.
