---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

If we choose a value $0 \le \alpha \le 1$ as our Type 1 error rate,
then we can find the critical value from the normal distribution using R's
`qnorm()` function. The code below shows how to do this for left-tailed,
right-tailed, and two-tailed hypothesis tests.

```R
alpha <- 0.05                           # Replace with your alpha value
qnorm(p = alpha, lower.tail = TRUE)     # Critical value for a left-tailed test
qnorm(p = alpha, lower.tail = FALSE)    # Critical value for a right-tailed test
qnorm(p = alpha/2, lower.tail = FALSE)  # Critical value for a two-tailed test
```

We can also compute $p$-values from the normal distribution to compare to a
test statistic.  As an example, we'll use a test statistic of 2.67, but you can
substitute your test statistic's value instead.

We can find the $p$-value for this test statistic using R's `pnorm()` function.
Again, we show code for left-tailed, right-tailed, and two-tailed tests.

```R
test_statistic <- 2.67                       # Replace with your test statistic
pnorm(test_statistic, lower.tail = TRUE)     # p-value for a left-tailed test
pnorm(test_statistic, lower.tail = FALSE)    # p-value for a right-tailed test
2*pnorm(test_statistic, lower.tail = FALSE)  # p-value for a two-tailed test
```
