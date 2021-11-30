---
author: Krtin Juneja (KJUNEJA@falcon.bentley.edu)
---

We will use some fake data for the purposes of an example, but you can replace
it with your real data in the code below.  Consider an ice cream shop's sales
data over several weekends.

```R
num.transactions <- c(91, 134, 98, 105, 93, 89, 145, 132, 109,
                      94, 105, 99, 84, 128, 120, 115, 118)
days <- c("Fri", "Sun", "Sun", "Sat", "Fri", "Fri", "Sat", "Sun", "Sun",
          "Fri", "Sat", "Sat", "Fri", "Sun", "Fri", "Sat", "Sun")
```

Let's assume that you have already performed an ANOVA on this data, as shown
below. (If you're not familiar with ANOVA, see how to do a one-way ANOVA test.)
Let's assume that we chose $\alpha$ to be 0.05.

```R
model <- aov(num.transactions ~ days)
summary(model)
```

From the $p$-value in the `Pr(>F)` column, we can see that, at the 5%
significance level, there are significant differences between the mean number
of transactions at the ice cream shop across these weekend days.

We'll use the `LSD.test` function (Least Significant Difference) from R's
`agricolae` package to get the confidence intervals for each pair of days.
Let's use $\alpha=0.05$ again so that we get 95% confidence intervals.

```R
# install.packages("agricolae") # if you have not already done so
library(agricolae)

test <- LSD.test(model, alpha=0.05, "days")
test
```

The portion of this lengthy output on which to focus is the `$groups` section.
If the categories share a letter in the "groups" column, then their means are
not significantly different from each other. Therefore:

 * Sunday and Saturday share the letter "a," so we know that the number of
   transactions on these two days are not significantly different from each
   other.
 * The same goes for Saturday and Friday, which share the letter "b."
 * But Sunday and Friday do not share a letter, so the number of transactions
   on these two days is significantly different.
