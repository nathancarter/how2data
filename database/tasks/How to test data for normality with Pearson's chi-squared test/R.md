---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We're going to use some fake restaurant data,
but you can replace our fake data with your real data in the code below.
The values in our fake data represent the amount of money that customers spent
on a Sunday morning at the restaurant.

```R
# Replace your data here
spending <- c(34, 12, 19, 56, 54, 34, 45, 37, 13, 22, 65, 19,
              16, 45, 19, 50, 36, 23, 28, 56, 40, 61, 45, 47, 37)

mean(spending)
sd(spending)
```

We will now conduct a test of the following null hypothesis:
The data comes from a population that is normally distributed with mean 36.52 and standard deviation 15.77.

We will use a value $\alpha=0.05$ as our Type I error rate.
The `pearson.test()` function in the `nortest` package can perform Pearson's $\chi^2$ test for normality.

```R
# install.packages("nortest") # if you have not already done so
library(nortest)
pearson.test(spending)
```

The p-value is 0.6264, which is greater than $\alpha=0.05$, so we fail to reject our null hypothesis.
We would continue to operate under our original assumption that the data come from a normally distributed population.
