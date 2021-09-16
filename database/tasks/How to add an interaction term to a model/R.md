---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We're going to use the `ToothGrowth` dataset in R as example data.
It contains observations of tooth growth for guinea pigs who received various doses of
various supplements.  You would use your own data instead.

```R
df <- ToothGrowth
```

Let's model tooth length (`len`) based on the product of two predictors,
the supplement given (`supp`) and its dosage (`dose`).
We simply use the ordinary multiplication operator in R, written `*`, to express
the product of these two factors when creating the model, as shown below.

Note that `supp` is a categorical variable with two values, so the model will
include a binary variable for whether the supplement was equal to "VC."

```R
# Build the model
model <- lm(len ~ supp*dose, data = df)
summary(model)
```

Now we have a model of the form $\hat L = 11.55 - 8.255s + 7.811d + 3.904sd$,
where $L$ stands for tooth length, $s$ for whether the VC supplement was given,
and $d$ for the dose given.
