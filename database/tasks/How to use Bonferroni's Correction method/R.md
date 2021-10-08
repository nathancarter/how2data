---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

Let's assume that you have already done an analysis of variance (ANOVA).
(See how to do a one-way analysis of variance (ANOVA) for details.)

As an example, we will use the fake data below, which looks at the number of
transactions at an ice cream shop on the weekends.
Let's assume that we chose $\alpha$ to be 0.05 in that ANOVA.

```R
# Store our fake data in vectors.  (You can replace this with your real data.)
num.transactions <- c(91, 134, 98, 105, 93, 89, 145, 132, 109,
                      94, 105, 99, 84, 128, 120, 115, 118)
days <- c("Fri", "Sun", "Sun", "Sat", "Fri", "Fri", "Sat", "Sun", "Sun",
          "Fri", "Sat", "Sat", "Fri", "Sun", "Fri", "Sat", "Sun")

# Perform an ANOVA and print a summary.
model <- aov(num.transactions ~ days)
summary(model)
```

The top-right value in the output is the $p$-value for the test, $0.034$.
Because it is below our chosen significance level of $\alpha=0.05$, there are
significant differences between the mean number of transactions at the ice cream
shop across at least two of these weekend days. But specifically which two, or
is it more than two?

We'll use the `PostHocTest()` function in the `DescTools` package, and specify
that we want to use the Bonferroni method to make the confidence intervals for
each pair of days. Let's let $\alpha$ be equal to 0.05 again, but the Bonferroni
correction implies that the overall probability of a Type I Error in *any* of
the tests below is now at most 0.05, rather than each one being 0.05 separately.

```R
# install.packages("DescTools") # If you have not already installed it
library(DescTools)

# Run the test and print the confidence intervals for each pair of days
PostHocTest(model, method = "bonferroni", conf.level = 0.95)
```

In the output, R has highlighted the second row for us by placing a `*` after
it.  That is the one row where the $p$-value (in the final column) is below our
chosen $\alpha=0.05$.

Therefore, the only significant difference in mean number of transactions is
between Sundays and Fridays. Notice also that the confidence interval in that
row (from `lwr.ci` to `upr.ci`) does not include zero. (In that particular row,
the confidence interval is $(1.076232,48.25710)$.)
