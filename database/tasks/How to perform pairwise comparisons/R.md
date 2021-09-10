---
author: Krtin Juneja (KJUNEJA@falcon.bentley.edu)
---

The solution below uses an example dataset that details the counts of insects
in an agricultural experiment with six types of insecticides, labeled A through F.
(This is one of the datasets built into R for use in examples like this one.)

```R
df <- InsectSprays
head( df, 10 )
```

Before we perform any post hoc analysis, we need to see if the count of insects
depends on the type of insecticide given by conducting a one way ANOVA.
(See also how to do a one-way analysis of variance (ANOVA).)

```R
aov1 = aov(count ~ spray, data = df)
summary(aov1)
```

At the 5% significance level, we see that the count differs according to the
type of insecticide used. We assume that the model assumptions are met,
but do not verify that here.

If we would like to compare the pairs without any corrections,
we can use the `pairwise.t.test` function built into R.

```R
pairwise.t.test(df$count, df$spray, p.adj="none")
```

Techniques to adjust the above table for multiple comparisons include
the Bonferroni correction, Fisher’s Least Significant Difference (LSD) method,
Dunnett’s procedure, and Scheffe’s method.
These can be used in place of "none" for the `p.adj` argument;
[see details here](https://www.rdocumentation.org/packages/stats/versions/3.6.2/topics/pairwise.t.test).

You can also determine the magnitude of these differences;
see how to perform post-hoc analysis with Tukey's HSD test.
