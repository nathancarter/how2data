---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

Let's say we have a dataset with the previous population proportions for four categories.
(This is contrived data, but the code below can be used on your actual data.)

| Category | Frequency | Proportion |
|----------|-----------|------------|
|    A     |    43     |    0.25    |
|    B     |    62     |    0.36    |
|    C     |    52     |    0.30    |
|    D     |    16     |    0.09    |

We have also taken a more recent sample and found the number of observations from it
that belong to each category. We want to determine if the proportions
coming from the recent sample are equal to the previous proportions.

R expects that we will have two vectors, one with the expected number of observations
in each group (from the previous, or hypothesized proportions) and the other with
the actual number of observations in each group (from the more recent sample).
R also expects that the total number of observations in each vector is the same.
We'll create two vectors below with the fake data from above,
but you can replace them with your real data

```R
# our fake data:
old.observations <- c(43, 62, 52, 16)
new.observations <- c(56, 80, 12, 25)
# now organized into a data frame:
categories <- c("A", "B", "C", "D")
data <- data.frame(categories, old.observations, new.observations)
```

We set the null hypothesis to be that the proportions of each category
from the recent sample are equal to the previous proportions.

$$H_0: p_A = 0.25\text{ and }\ p_B = 0.36\text{ and }\ p_C = 0.30\text{ and }\ p_D=0.09.$$

We choose a value $0 \le \alpha \le 1$ as our Type 1 error rate.
We'll let $\alpha$ be 0.05 here.

```R
# Run the Chi-Square test, giving the test statistic and p-value
chisq.test(data$new.observations, p=data$old.observations, rescale.p=TRUE)
```

Our $p$-value is less than $\alpha$, so we have sufficient evidence to reject the null hypothesis.
It does appear that the proportion of at least one of the four categories
is significantly different now from what it was previously.

If instead you provided the population proportions as the old observations,
that is, a vector of values that sum to 1, you can omit the `rescale.p` argument.
