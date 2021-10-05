---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

If we choose a value $0 \le \alpha \le 1$ as our Type 1 error rate,
and we know the sample size of our data,
then we can find the *critical value* from the $t$-distribution using R's
`qt()` function. The code below shows how to do this for left-tailed,
right-tailed, and two-tailed hypothesis tests.

```R
alpha <- 0.05                                  # Replace with your alpha value
n <- 68                                        # Replace with your sample size
qt(p = alpha, df = n-1, lower.tail = TRUE)     # Critical value for a left-tailed test
qt(p = alpha, df = n-1, lower.tail = FALSE)    # Critical value for a right-tailed test
qt(p = alpha/2, df = n-1, lower.tail = FALSE)  # Critical value for a two-tailed test
```

We can also compute $p$-values from the $t$-distribution to compare to a
test statistic.  As an example, we'll use a test statistic of 2.67, but you can
substitute your test statistic's value instead.

We can find the $p$-value for this test statistic using R's `pt()` function.
We will use the same example sample size as above.
Again, we show code for left-tailed, right-tailed, and two-tailed tests.

```R
test_statistic <- 2.67                              # Replace with your test statistic
n <- 68                                             # Replace with your sample size
pt(test_statistic, df = n-1, lower.tail = TRUE)     # p-value for a left-tailed test
pt(test_statistic, df = n-1, lower.tail = FALSE)    # p-value for a right-tailed test
2*pt(test_statistic, df = n-1, lower.tail = FALSE)  # p-value for a two-tailed test
```
