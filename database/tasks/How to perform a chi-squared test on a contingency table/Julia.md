---
author: Nathan Carter (ncarter@bentley.edu)
---

Here we will use a two-dimensional Julia array to store a contingency table of
education vs. gender, taken from
[Penn State University's online stats review website](https://online.stat.psu.edu/statprogram/reviews/statistical-concepts/chi-square-tests).
You should use your own data.

```julia
data = [
#   HS  BS  MS  Phd
    60  54  46  41    # females
    40  44  53  57    # males
]
```

The $\chi^2$ test's null hypothesis is that the two variables are independent.
We choose a value $0\leq\alpha\leq1$ as the probability of a Type I error
(false positive, finding we should reject $H_0$ when it's actually true).

```julia
alpha = 0.05  # or choose your own alpha here

using HypothesisTests
p_value = pvalue( ChisqTest( data ) )
reject_H0 = p_value < alpha
alpha, p_value, reject_H0
```

In this case, the samples give us enough evidence to reject the null hypothesis
at the $\alpha=0.05$ level.  The data suggest that the two categorical variables
are not independent.

If you are using the most common $\alpha$ value of $0.05$, you can save a few lines
of code and get more output by just writing the test itself:

```julia
ChisqTest( data )
```
