---
author: "Krtin Juneja (KJUNEJA@falcon.bentley.edu)"
---

We use a built-in dataset called `ToothGrowth` that discusses
the length of the teeth (`len`) in each of 10 guinea pigs
at three Vitamin C dosage levels ($0.5$, $1$, and $2$ mg)
with two delivery methods - orange juice or ascorbic acid (`supp`).

```R
# You can replace this example data frame with your own data
df <- ToothGrowth
```

If you wish to understand the distribution of the length of the tooth
based on the delivery methods, you can construct a bivariate histogram plot.

```R
# install.packages( "lattice" ) # if you have not already done this
library(lattice)
histogram( ~ len | supp, data = df)
```

To visualize the summary statistics of the length of the tooth
based on the delivery methods, you can construct a bivariate box plot.

```R
bwplot(df$len ~ df$supp)
# Or the following code produces a similar figure, using the mosaic package:
# boxplot(len ~ supp, data = df)
```

To plot the means for both treatment levels of `supp` for the `len` column,
we load the `gplots` package and use the `plotmeans` function.

```R
# install.packages( "gplots" ) # if you have not already done this
library(gplots)
plotmeans(df$len ~ df$supp)
```
