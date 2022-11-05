---
author: Nathan Carter (ncarter@bentley.edu)
---

This is a two-sided test with the null hypothesis $H_0:\mu=\bar x$.
We choose a value $0\leq\alpha\leq1$ as the probability of a Type I error
(false positive, finding we should reject $H_0$ when it's actually true).

```julia
# Replace these first three lines with the values from your situation.
alpha = 0.05
pop_mean = 10
sample = [ 9, 12, 14, 8, 13 ]

# The following code runs the test for your chosen alpha:
using HypothesisTests
p_value = pvalue( OneSampleTTest( sample, pop_mean ) )
reject_H0 = p_value < alpha
alpha, p_value, reject_H0
```

In this case, the $p$-value was larger than $\alpha$, so the sample does not give us
enough information to reject the null hypothesis.
We would continue to assume that the sample is like the population, $\mu=\bar x$.

When you are using the most common value for $\alpha$, which is $0.05$ for the $95\%$
confidence interval, you can simply print out the test itself and get a detailed
printout with all the information you need, thus saving a few lines of code.

```julia
OneSampleTTest( sample, pop_mean )
```
