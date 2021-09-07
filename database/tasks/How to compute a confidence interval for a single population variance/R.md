---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We'll use R's dataset EuStockMarkets here. This dataset has information on the daily closing prices of 4 European stock indices. We're going to look at the variability of Germany's DAX closing prices. Feel free to replace this sample data with your actual data if you use this
code.

```R
# install.packages("datasets") # if you have not done so already
library(datasets)

# Load stock market data, convert to DataFrame, and choose the DAX column.
EuStockMarkets <- data.frame(EuStockMarkets)
sample <- EuStockMarkets$DAX
```

Now that we have our sample data loaded, let's go ahead and make the confidence interval.

```R
# Find the critical values from the right and left tails of the Chi-square distribution
alpha = 0.05       # replace with your chosen alpha (here, a 95% confidence level)
n <- length(sample)
left_critical_val <- qchisq(p = alpha/2, df = n-1, lower.tail=FALSE)
right_critical_val <- qchisq(p = 1-alpha/2, df = n-1, lower.tail=FALSE)

# Find the upper and lower bounds of the confidence interval and print them out
lower_bound <- ((n - 1)*var(sample))/left_critical_val
upper_bound <- ((n - 1)*var(sample))/right_critical_val
lower_bound
upper_bound
```

Our 95% confidence interval for the standard deviation
of Germany's DAX closing prices is $[1104642, 1256248]$.
