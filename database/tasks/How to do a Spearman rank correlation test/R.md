---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We will use some fake data about height and weight measurements for people.
You can replace it with your real data.

Our data should be stored in R vectors, as shown below.

```R
heights <- c(60, 76, 57, 68, 70, 62, 63)
weights <- c(145, 178, 120, 143, 174, 130, 137)
```

Let's say we want to test the correlation between height (inches) and weight (pounds). 
Our null hypothesis would state that the Pearson correlation coefficient is equal to zero,
or that there is no relationship between height and weight, $H_0: \rho_s = 0$.
We choose $\alpha$, or the Type I error rate, to be 0.05 and carry out the
Spearman Rank Correlation Test to get the test-statistic and $p$-value.

```R
# Run the Spearman Rank Correlation Test to get the test-statistic and p-value
cor.test(heights, weights, alternative = "two.sided", method = "spearman")
```

Our $p$-value is $0.04802$, which is less than $\alpha=0.05$, so we reject the null hypothesis.
There does appear to be a relationship between height and weight.

(This $p$-value is different than the one computed in the solution using Python,
because different approximation methods are used by the two software packages
when the sample size is small.)

Note that for a right-tailed test, you can replace "two.sided" with "greater"
and for a left-tailed test, you can replace "two.sided" with "less".
