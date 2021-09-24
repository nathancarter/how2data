---
author: Nathan Carter (ncarter@bentley.edu)
---

Here we will use a $2\times4$ matrix to store a contingency table of
education vs. gender, taken from
[Penn State University's online stats review website](https://online.stat.psu.edu/statprogram/reviews/statistical-concepts/chi-square-tests).
You should use your own data.
(Note: R's `table` function is useful for creating contingency tables from data.)

```R
data <- matrix( c( 60, 54, 46, 41, 40, 44, 53, 57 ), ncol = 4,
                dimnames=list( c('F','M'), c('HS','BS','MS','PhD') ),
                byrow =TRUE)
data
```

The $\chi^2$ test's null hypothesis is that the two variables are independent.
We choose a value $0\leq\alpha\leq1$ as the probability of a Type I error
(false positive, finding we should reject $H_0$ when it's actually true).

R provides a `chisq.test` function that does exactly what we need.

```R
results <- chisq.test( data )
results
```

We can manually compare the $p$-value to an $\alpha$ we've chosen, or ask R to do it.

```R
alpha <- 0.05            # or choose your own alpha here
results$p.value < alpha  # reject the null hypothesis?
```
