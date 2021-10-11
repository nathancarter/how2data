---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We will use some fake data in this example, but you can replace it with your
real data.  Imagine we conduct a survey of people in Boston and of people in Nashville
and ask them if they prefer chocolate or vanilla ice cream. We get data like the
following.

|    City   | Prefer chocolate | Prefer vanilla | Total |
|-----------|------------------|----------------|-------|
|   Boston  |        60        |       90       |  150  |
| Nashville |        85        |       50       |  135  |

We want to compare the proportions of people from the two cities who like vanilla.

Let $\bar{p}_1$ represent the proportion of people from Boston who like vanilla
and $\bar{p}_2$ represent the proportion of people from Nashville who like vanilla.

```R
n1 <- 150
n2 <- 135
p_bar1 <- 90/150
p_bar2 <- 50/135
```

We choose a value $0 \le \alpha \le 1$ as our Type 1 error rate.
For this example, we will use $\alpha=0.05$.

### Two-tailed test

In a two-tailed test, the null hypothesis states that the difference between the
two proportions equals a hypothesized value; let's choose zero,
$H_0: \bar{p}_1 - \bar{p}_2 = 0$.  We perform this test
by computing a test statistic and $p$-value as shown below, then comparing the
$p$-value to our chosen $\alpha$.

```R
p_bar <- (90 + 50) / (150 + 135)                 # overall proportion
std_error <- sqrt(p_bar*(1-p_bar)*(1/n1+1/n2))   # standard error
test_statistic <- (p_bar1 - p_bar2)/std_error    # test statistic
2*pnorm(q = test_statistic, lower.tail = FALSE)  # two-tailed p-value
```

Our $p$-value, 0.000108, is smaller than $\alpha$, so we can reject the null
hypothesis and conclude that the difference between the two proportions is
different from zero.

But we did not need to compare the difference to zero; we could have used any
hypothesized difference for comparison.  Let's repeat the above test, comparing
the difference to $0.15$ instead, as an example.

```R
hyp.diff = 0.15                                             # hypothesized difference
std_error <- sqrt(p_bar1*(1-p_bar1)/n1
                + p_bar2*(1-p_bar2)/n2)                     # standard error
test_statistic <- ((p_bar1 - p_bar2) - hyp.diff)/std_error  # test statistic
2*pnorm(q = test_statistic, lower.tail = FALSE)             # two-tailed p-value
```

Our $p$-value, 0.1674, is greater than $\alpha$, so we cannot reject the null hypothesis
and cannot conclude that the difference between these two proportions is significantly
different from 0.15.

### Right-tailed test

In a right-tailed test, the null hypothesis states that the difference between
the two proportions is less than or equal to a hypothesized value.  Let's begin
by using zero as our hypothesized value, $H_0: \bar{p}_1 - \bar{p}_2 \le 0$.

We repeat some code below that we've seen above, just to make it easy to copy and
paste the example elsewhere.

```R
p_bar <- (90 + 50) / (150 + 135)                 # overall proportion
std_error <- sqrt(p_bar*(1-p_bar)*(1/n1+1/n2))   # standard error
test_statistic <- (p_bar1 - p_bar2)/std_error    # test statistic
pnorm(q = test_statistic, lower.tail = FALSE)    # right-tailed p-value
```

Our $p$-value is smaller than $\alpha$, so we can reject the null hypothesis and
conclude that the difference between the two proportions is significantly greater than zero.

But we did not need to compare the difference to zero; we could have used any
hypothesized difference for comparison.  Let's repeat the above test, comparing
the difference to $0.15$ instead, as an example.

```R
hyp.diff = 0.15                                             # hypothesized difference
std_error <- sqrt(p_bar1*(1-p_bar1)/n1
                + p_bar2*(1-p_bar2)/n2)                     # standard error
test_statistic <- ((p_bar1 - p_bar2) - hyp.diff)/std_error  # test statistic
pnorm(q = test_statistic, lower.tail = FALSE)               # right-tailed p-value
```

Our $p$-value, 0.0837, is greater than $\alpha$, so we cannot reject the null
hypothesis and cannot conclude that the difference between these two proportions
is significantly greater than 0.15.

### Left-tailed test

In a left-tailed test, the null hypothesis states that the difference between
the two proportions is greater than or equal to a hypothesized value.  Let's begin
by using zero as our hypothesized value, $H_0: \bar{p}_1 - \bar{p}_2 \ge 0$.

We repeat some code below that we've seen above, just to make it easy to copy and
paste the example elsewhere.

```R
p_bar <- (90 + 50) / (150 + 135)                 # overall proportion
std_error <- sqrt(p_bar*(1-p_bar)*(1/n1+1/n2))   # standard error
test_statistic <- (p_bar1 - p_bar2)/std_error    # test statistic
pnorm(q = test_statistic, lower.tail = TRUE)     # left-tailed p-value
```

Our $p$-value, 0.9999, is greater than $\alpha$, so we cannot reject the null
hypothesis and cannot conclude that the difference between the two proportions
is significantly less than zero.

But we did not need to compare the difference to zero; we could have used any
hypothesized difference for comparison.  Let's repeat the above test, comparing
the difference to $0.15$ instead, as an example.

```R
hyp.diff = 0.15                                             # hypothesized difference
std_error <- sqrt(p_bar1*(1-p_bar1)/n1
                + p_bar2*(1-p_bar2)/n2)                     # standard error
test_statistic <- ((p_bar1 - p_bar2) - hyp.diff)/std_error  # test statistic
pnorm(q = test_statistic, lower.tail = TRUE)                # left-tailed p-value
```

Our $p$-value, 0.91627, is greater than $\alpha$, so we cannot reject the null
hypothesis and cannot conclude that the difference between these two proportions
is significantly less than 0.15.
