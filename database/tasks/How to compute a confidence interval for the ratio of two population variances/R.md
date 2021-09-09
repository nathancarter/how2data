---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We'll use R's dataset EuStockMarkets as an example; of course you should replace this example data with your actual data when using this code. This dataset has information on the daily closing prices of 4 European stock indices. We're going to compare the variability of Germany's DAX and France's CAC closing prices here.

```R
# install.packages("datasets") # if you have not done so already
library(datasets)

# Load in the EuStockMarkets data and convert to a DataFrame
EuStockMarkets <- data.frame(EuStockMarkets)

# Our two samples are its DAX and CAC columns
sample.1 <- EuStockMarkets$DAX
sample.2 <- EuStockMarkets$CAC
```

Now that we have our data loaded we can compute the confidence interval. You can change the confidence level by changing the value of $\alpha$ below.

```R
# The degrees of freedom in each sample is its length minus 1
df_1 = length(sample.1) - 1
df_2 = length(sample.2) - 1

# Compute the ratio of the variances
test.stat.ratio <- var(sample.1)/var(sample.2)

# Find the critical values from the F-distribution
alpha <- 0.05       # replace with your chosen alpha (here, a 95% confidence level)
lower_critical_value <- 1 / qf(p = alpha/2, df1 = df_1, df2 = df_2, lower.tail = FALSE)
upper_critical_value <- qf(p = alpha/2, df1 = df_2, df2 = df_1, lower.tail = FALSE)

# Compute the confidence interval and print it out
lower_bound <- test.stat.ratio*lower_critical_value
upper_bound <- test.stat.ratio*upper_critical_value
lower_bound
upper_bound
```

The 95% confidence interval for the ratio of the variances for Germany's DAX and France's CAC is $[3.191, 3.827]$.