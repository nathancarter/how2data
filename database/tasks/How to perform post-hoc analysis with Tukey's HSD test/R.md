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
the magnitudes of the differences between pairs of groups. We do this by
applying Tukey's HSD approach to perform pairwise comparisons and generate
confidence intervals that maintain a specified experiment-wide error rate.
We use R's built-in `TukeyHSD` function, and we give it the same ANOVA results
that we computed in the solution for how to perform pairwise comparisons.

```R
aov1 <- aov(count ~ spray, data = df)
TukeyHSD(aov1, "spray", ordered=TRUE, conf.level = 0.95)
```

Because the above table contains a lot of information, it's often helpful to
visualize these intervals. R lets us do so by simply calling `plot` on the
above table. We add a few plotting parameters to improve its appearance.

```R
plot( TukeyHSD(aov1, "spray", ordered=TRUE, conf.level = 0.95),
      las=1, cex.axis=0.9 )
```

Confidence intervals that cross the vertical, dashed line at $x=0$ are those
in which the means across those groups may be equal.  Other intervals have
mean differences whose 95% confidence intervals do not include zero.
