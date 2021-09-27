---
author: Nathan Carter (ncarter@bentley.edu)
---

This is a two-sided test with the null hypothesis $H_0:\mu=\bar x$.
We choose a value $0\leq\alpha\leq1$ as the probability of a Type I error
(false positive, finding we should reject $H_0$ when it's actually true).

```R
# Replace these first three lines with the values from your situation.
alpha <- 0.05
pop.mean <- 10
sample <- c( 9, 12, 14, 8, 13 )

# Run a one-sample t-test and print out alpha, the p value,
# and whether the comparison says to reject the null hypothesis.
t.test( sample, mu=pop.mean, conf.level=1-alpha )
```

Although we can deduce the answer to our question from the above output,
by comparing the $p$ value with $\alpha$ manually, we can also ask R
to do it.

```R
# Is there enough evidence to reject the null hypothesis?
result <- t.test( sample, mu=pop.mean, conf.level=1-alpha )
result$p.value < alpha
```

In this case, the sample does not give us enough information to reject
the null hypothesis.  We would continue to assume that the sample is like
the population, $\mu=\bar x$.
