---
author:
 - Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
 - Nathan Carter (ncarter@bentley.edu)
---

Let's assume that you already fit the linear model, as shown in the code below.
This one uses a small amount of fake data, but it's just an example.
See also how to fit a linear model to two columns of data.

```R
x <- c(34, 9, 78, 60, 22, 45, 83, 59, 25)
y <- c(126, 347, 298, 309, 450, 187, 266, 385, 400)
model <- lm(y ~ x)
```

The standard error for each estimate is shown as part of the model summary, reported by R's
built-in `summary` function.  See the column entitled "Std. Error" in the output below.

```R
summary(model)
```

If we need to extract just the model coefficients table, or even just the "Std. Error"
column of it, we can use code like the following.

```R
coef(summary(model))
coef(summary(model))[,2]
```

The standard error of the estimate for the intercept is is 76.733 and
the standard error of the estimate for the slope is 1.473.
