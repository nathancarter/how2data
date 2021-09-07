---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We'll assume that you have fit a single linear model to your data, as in the code below,
which uses fake example data.  You can replace it with your actual data.

```R
x <- c(34, 9, 78, 60, 22, 45, 83, 59, 25)
y <- c(126, 347, 298, 309, 450, 187, 266, 385, 400)
model <- lm(y ~ x)
```

We can use R's `confint()` function to find the confidence interval for the model coefficients. You can change the `level` parameter to specify a different confidence level. Note that if you have a multiple regression model, it will make confidence intervals for all of the coefficient values.

```R
# Compute confidence intervals for the model
confint(model, level = 0.95)   # Assuming a confidence level of 0.95
```

The 95% confidence interval for the regression coefficient is $[-4.491961, 2.473935]$.
