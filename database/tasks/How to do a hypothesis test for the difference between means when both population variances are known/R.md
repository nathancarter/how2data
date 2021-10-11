---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We're going to use fake data here, but you can replace our fake data with your real data below.
You will need not only the samples but also the known population standard deviations.

```R
sample1 <- c(5, 8, 10, 3, 6, 2)
sample2 <- c(13, 20, 16, 12, 18, 15)
population1_sd = 2.4
population2_sd = 3
```

We must compute the sizes and means of the two samples.

```R
n1 <- length(sample1)
n2 <- length(sample2)
sample1_mean <- mean(sample1)
sample2_mean <- mean(sample2)
```

We choose a value $0 \le \alpha \le 1$ as the probability of a Type I error
(a false positive, finding we should reject $H_0$ when it’s actually true).
We will use $\alpha=0.05$ in this example.

### Two-tailed test

In a two-tailed test, the null hypothesis is that the difference is zero,
$H_0: \bar{x} - \bar{x}' = 0$.  We compute a test statistic and $p$-value as
follows.

```R
test_statistic <- (sample1_mean - sample2_mean) /
    sqrt(population1_sd^2/n1 + population2_sd^2/n2)
2*pnorm(abs(test_statistic), lower.tail = FALSE)  # two-tailed p-value
```

Our p-value is less than $\alpha$, so we have sufficient evidence to reject the null hypothesis.
The difference between the means is significantly different from zero.

### Right-tailed test

In the right-tailed test, the null hypothesis is $H_0: \bar{x} - \bar{x}' \le 0$.
That is, we are testing whether the difference is greater than zero.

The code is very similar to the previous, except only in computing the $p$-value.
We repeat the code that's in common, to make it easier to copy and paste the examples.

```R
test_statistic <- (sample1_mean - sample2_mean) /
    sqrt(population1_sd^2/n1 + population2_sd^2/n2)
pnorm(test_statistic, lower.tail = FALSE)  # right-tailed p-value
```

Our $p$-value is greater than $\alpha$, so we do not have sufficient evidence to
reject the null hypothesis. We would continue to assume that the difference in
means is less than or equal to zero.

### Left-tailed test

In a left-tailed test, the null hypothesis is $H_0: \bar{x} - \bar{x}' \ge 0$.
That is, we are testing whether the difference is less than zero.

The code is very similar to the previous, except only in computing the $p$-value.
We repeat the code that's in common, to make it easier to copy and paste the examples.

```R
test_statistic <- (sample1_mean - sample2_mean) /
    sqrt(population1_sd^2/n1 + population2_sd^2/n2)
pnorm(test_statistic, lower.tail = TRUE)  # left-tailed p-value
```

Our $p$-value is less than $\alpha$, so we have sufficient evidence to reject
the null hypothesis. The difference between the means is significantly less than zero.
