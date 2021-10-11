---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We're going to use fake data here for illustrative purposes,
but you can replace our fake data with your real data in the code below.

Let's say that we've hypothesized that about one-third of Bostonians are unhappy
with the Red Sox' performance.
To test this hypothesis, we surveyed 460 Bostonians and found that 76 of them
were unhappy with the Red Sox' performance.

We summarize this situation with the following variables.
We will do a test with a Type I error rate of $\alpha=0.05$.

```R
n <- 460               # Number of respondents in sample
x <- 76                # Number of respondents in chosen subset
population_prop <- 1/3 # Hypothesized population proportion
```

### Two-tailed test

A two-tailed test is for the null hypothesis $H_0: p = \frac13$.
We use R's `prop.test()` function and provide it the data from above,
requesting a two-tailed test.

```R
prop.test(x = x, n = n, p = population_prop, alternative = "two.sided")
```

The $p$-value (shown at the end of the third line of the output)
is less than $\alpha$, so we can reject the null hypothesis.
The proportion of Bostonians unhappy with Red Sox performance is different from $\frac13$.

R also has a `binom.test()` function that takes the same arguments.

### Right-tailed test

A right-tailed test is for the null hypothesis $H_0: p \le \frac13$.
We use R's `prop.test()` function and provide it the data from above,
requesting a right-tailed test.

```R
prop.test(x = x, n = n, p = population_prop, alternative = "greater")
```

The $p$-value (shown at the end of the third line of the output)
is greater than $\alpha$, so we cannot reject the null hypothesis.
We continue to assume that the proportion of Bostonians unhappy with Red Sox
performance is less than or equal to $\frac13$.

Again, `binom.test()` takes the same arguments.

### Left-tailed test

A left-tailed test is for the null hypothesis $H_0: p\ge \frac13$.
We use R's `prop.test()` function and provide it the data from above,
requesting a left-tailed test.

```R
prop.test(x = x, n = n, p = population_prop, alternative = "less")
```

The $p$-value (shown at the end of the third line of the output)
is less than $\alpha$, so we can reject the null hypothesis.
The proportion of Bostonians unhappy with Red Sox performance is less than $\frac13$.

Again, `binom.test()` takes the same arguments.
