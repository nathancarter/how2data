---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

If we call the mean of the first sample $\bar x_1$
and the mean of the second sample $\bar x_2$,
then this is a left-tailed test with the null hypothesis
$H_0: \bar x_1 - \bar x_2 \ge 0$.
We choose a value $0 \le \alpha \le 1$ as the probability of a Type I error
(false positive, finding we should reject $H_0$ when it’s actually true).

```R
# Replace these first three lines with the values from your situation.
alpha <- 0.10
sample1 <- c( 6, 9, 7, 10, 10, 9 )
sample2 <- c( 12, 14, 10, 17, 9 )

# Run a one-sample t-test and print out alpha, the p value,
# and whether the comparison says to reject the null hypothesis.
t.test( sample1, sample2, conf.level=1-alpha, alternative = "less" )
```

Although we can deduce the answer to our question from the above output,
by comparing the $p$-value with $\alpha$  manually, we can also ask R to do it.

```R
# Is there enough evidence to reject the null hypothesis?
result <- t.test( sample1, sample2, conf.level=1-alpha, alternative = "less" )
result$p.value < alpha
```

In this case, the samples give us enough evidence to reject the null hypothesis
at the $\alpha=0.10$ level. The data suggest that $\bar x_1 < \bar x_2$.

Here we did not assume that the two samples had equal variance.
If in your case they do, you can pass the parameter `var.equal=TRUE` to `t.test`.
