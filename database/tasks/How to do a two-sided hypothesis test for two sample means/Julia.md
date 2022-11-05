---
author: Nathan Carter (ncarter@bentley.edu)
---

If we call the mean of the first sample $\bar x_1$ and the mean of the
second sample $\bar x_2$, then this is a two-sided test
with the null hypothesis $H_0:\bar x_1=\bar x_2$.
We choose a value $0\leq\alpha\leq1$ as the probability of a Type I error
(false positive, finding we should reject $H_0$ when it's actually true).

```julia
# Replace these first three lines with the values from your situation.
alpha = 0.10
sample1 = [ 6, 9, 7, 10, 10, 9 ]
sample2 = [ 12, 14, 10, 17, 9 ]

# Run a one-sample t-test and print out alpha, the p value,
# and whether the comparison says to reject the null hypothesis.
using HypothesisTests
p_value = pvalue( UnequalVarianceTTest( sample1, sample2 ) )
reject_H0 = p_value < alpha
alpha, p_value, reject_H0
```

In this case, the $p$-value was less than $\alpha$, so the sample gives us
enough evidence to reject the null hypothesis at the $\alpha=0.10$ level.
The data suggest that $\bar x_1\neq\bar x_2$.

When you are using the most common value for $\alpha$, which is $0.05$ for the $95\%$
confidence interval, you can simply print out the test itself and get a detailed
printout with all the information you need, thus saving a few lines of code.
Note that this gives a different answer below than the one above, because above we
chose to use $\alpha=0.10$, but the default below is $\alpha=0.05$.

```julia
UnequalVarianceTTest( sample1, sample2 )
```

Here we did not assume that the two samples had equal variance.
If in your case they do, you can use `EqualVarianceTTest()` instead of
`UnequalVarianceTTest()`.
