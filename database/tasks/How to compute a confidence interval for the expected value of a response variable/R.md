---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

Let's assume that you already have a linear model.  We construct an example one here from some fabricated data.

```R
# Make the linear model
x <- c(34, 9, 78, 60, 22, 45, 83, 59, 25)
y <- c(126, 347, 298, 309, 450, 187, 266, 385, 400)
model <- lm(y ~ x)
```

Construct a data frame containing just one entry, the value of the independent variable for which you want to compute the confidence interval.
That data frame can then be passed to R's `predict` function to get a confidence interval for the expected value of $y$.

```R
# Use your chosen value of x below:
data <- data.frame(x=40)
# Compute the confidence interval for y:
predict(model, data, interval="confidence", level=0.95) # or choose a different confidence level; here we use 0.95
```

Our 95% confidence interval is $[226.648, 400.7954]$. We can be 95% confident that the true average value of $y$, given that $x$ is 40, is between 226.648 and 400.7954.
