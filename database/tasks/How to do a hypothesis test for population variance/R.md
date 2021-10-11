---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We'll use R's dataset `EuStockMarkets` to do an example. This dataset has
information on the daily closing prices of 4 European stock indices.
We're going to look at the variability of Germany's DAX closing prices.

Let's load the dataset.  (See how to quickly load some sample data.)
If using your own data, place it into the `values` variable instead of using
the code below.

```R
# install.packages("datasets") # If you have not already done this
library(datasets)
EuStockMarkets <- data.frame(EuStockMarkets)
values <- EuStockMarkets$DAX
```

### Two-tailed test

We may ask whether the population variance is significantly different from a
hypothesized value.  Let's test against a variance of 1,000,000.

Our null hypothesis states that the population variance is equal to 1,000,000,
$H_0: \sigma^2 = 1,000,000$.  We calculate the test statistic and $p$-value as
follows, using a $\chi^2$ distribution.  We can use any $\alpha$ between 0.0 and
1.0 as our Type I Error Rate; we will use $\alpha=0.05$ here.

```R
hyp.var <- 1000000                                # hypothesized variance
df <- length(values) - 1                          # degrees of freedom
test.statistic <- df*var(values)/hyp.var          # test statistic
2*pchisq(test.statistic, df=df, lower.tail=FALSE) # two-tailed p-value
```

Our $p$-value, $3.189769\times10^{-7}$, is smaller than $\alpha$, so we have
sufficient evidence to reject the null hypothesis. The variance of closing
prices on Germany's DAX is signficantly different from 1,000,000.

### Left-tailed test

What if we wanted to determine if the population variance were significantly
less than 1,000,000? Our null hypothesis would therefore be
$H_0: \sigma^2 \ge 1,000,000$.

The computations are very similar to the previous case, but with a different
formula for the $p$-value.  We repeat the code that's in common, for ease of use
when copying and pasting.

```R
hyp.var <- 1000000                             # hypothesized variance
df <- length(values) - 1                       # degrees of freedom
test.statistic <- df*var(values)/hyp.var       # test statistic
pchisq(test.statistic, df=df, lower.tail=TRUE) # left-tailed p-value
```

Our p-value, 0.9999998, is greater than $\alpha$, so we do not have sufficient
evidence to reject the null hypothesis. We should continue to assume that the
variance of closing prices on Germany's DAX is greater than or equal to
1,000,000.

### Right-tailed test

What if we wanted to determine if the population variance were significantly
less than 1,000,000? Our null hypothesis would therefore be
$H_0: \sigma^2 \ge 1,000,000$.

The computations are very similar to the previous case, but with a different
formula for the $p$-value.  We repeat the code that's in common, for ease of use
when copying and pasting.

```R
hyp.var <- 1000000                              # hypothesized variance
df <- length(values) - 1                        # degrees of freedom
test.statistic <- df*var(values)/hyp.var        # test statistic
pchisq(test.statistic, df=df, lower.tail=FALSE) # right-tailed p-value
```

Our p-value, $1.594884\times10^{-7}$, is smaller than $\alpha$, so have
sufficient evidence to reject the null hypothesis. We conclude that the
variance of closing prices on Germany's DAX is significantly greater than
1,000,000.
