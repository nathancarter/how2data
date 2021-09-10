---
author: "Krtin Juneja (kjuneja@falcon.bentley.edu)"
---

We load here the same data that appears in the solution for how to perform
pairwise comparisons. That solution used ANOVA to determine which pairs of
groups have significant differences in their means; follow its link for more
details.

```R
# Load an inbuilt data set called InsectSprays and assign it to the variable df
df <- InsectSprays
head( df, 10 )
```

We now want to perform an unplanned comparison test on the data to determine
the magnitudes of the differences between pairs of groups. Although R has a
built-in `TukeyHSD` function, its output is not as complete as the `HSD.test`
function in the agricolae package, so here we will use that latter function.
We provide it the same ANOVA results that we computed in the solution to
how to perform pairwise comparisons.

```R
# install.packages( "agricolae" ) # if you have not already done this
library(agricolae)
aov1 <- aov(count ~ spray, data = df)
HSD.test(aov1, "spray", group=FALSE, console=TRUE)
```

The table above highlights for us those confidence intervals whose means are
significantly different from zero, and provides other information as well.
To see if there is any statistical different between the pairs, look at the
"signif" column. The more asterisks appear there, the more significant the
difference.
