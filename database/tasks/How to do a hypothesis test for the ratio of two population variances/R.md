---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We'll use R's dataset `EuStockMarkets` to do an example. This dataset has
information on the daily closing prices of 4 European stock indices.
We're going to compare the variability of Germany's DAX and France's CAC
closing prices.

Let's load the dataset.  (See how to quickly load some sample data.)
If using your own data, place it into the `sample1` and `sample2` variables
instead of using the code below.

```R
# install.packages("datasets") # If you have not already done so
library(datasets)

# Load the dataset and convert it to a data frame, then extract two columns
EuStockMarkets <- data.frame(EuStockMarkets)
sample.1 <- EuStockMarkets$DAX
sample.2 <- EuStockMarkets$CAC
```

# Two-tailed test

For all tests below, we will use $\alpha=0.05$ as our Type I Error Rate, but any
value between 0.0 and 1.0 can be used.

### Two-tailed test

We can use a two-tailed test to test whether the two population variances are
equal.  Specifically, the null hypothesis will be:

$$H_0: \frac{\sigma_1^2}{\sigma_2^2} = 1$$

```R
sample.1.df <- length(sample.1) - 1            # degrees of freedom
sample.2.df <- length(sample.2) - 1            # degrees of freedom
test.statistic <- var(sample.1)/var(sample.2)  # test statistic
2*pf(test.statistic, df1=sample.1.df, df2=sample.2.df, lower.tail=FALSE) # p-value
```

Our $p$-value is smaller than our chosen alpha, so we have sufficient evidence
to reject the null hypothesis. The ratio of the variance of the closing prices
on Germany's DAX and France's CAC is significantly different than 1, so the
variances are not equal.

### Right-tailed test

In a right-tailed test, the null hypothesis is that the ratio is less than or
equal to 1.  This is equivalent to asking if $\sigma_1^2 \le \sigma_2^2$.

$$H_0: \frac{\sigma_1^2}{\sigma_2^2} \le 1$$

We repeat below some of the code above to make each example easy to copy and paste.

```R
sample.1.df <- length(sample.1) - 1            # degrees of freedom
sample.2.df <- length(sample.2) - 1            # degrees of freedom
test.statistic <- var(sample.1)/var(sample.2)  # test statistic
pf(test.statistic, df1=sample.1.df, df2=sample.2.df, lower.tail=FALSE) # p-value
```

Our $p$-value is smaller than our chosen alpha, so we have sufficient evidence
to reject the null hypothesis. The ratio of the variance of the closing prices
on Germany's DAX and France's CAC is significantly greater than 1, so the
variance of closing prices on Germany's DAX is greater than that of closing
prices on France's CAC.

To test whether $\sigma_1^2 \ge \sigma_2^2$, simply swap the roles of the two
data columns in the above code.