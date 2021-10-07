---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

Let's assume that you've already built a linear model.
We do an example below with fake data, but you can use your own actual data.
For more information on the following code, see
how to fit a multiple linear regression linear model.

```R
x1 <- c( 2,  7,  4,  3, 11, 18,   6, 15,   9,  12)
x2 <- c( 4,  6, 10,  1, 18, 11,   8, 20,  16,  13)
x3 <- c(11, 16, 20,  6, 14,  8,   5, 23,  13,  10)
y  <- c(24, 60, 32, 29, 90, 45, 130, 76, 100, 120)
model <- lm(y ~ x1 + x2 + x3)
```

Let's say we want to estimate $y$ given that  $x_1 = 5$, $x_2 = 12$, and $x_3=50$.
We can use R's `predict()` function as shown below.

```R
predict(model, newdata = data.frame(x1 = 5, x2 = 12, x3 = 50))
```

For the given values of the explanatory variables,
our predicted response variable is $-91.71014$.

Note that if you want to compute the predicted values for all the data
on which the model was trained, simply call `predict(model)` with no new data,
and it defaults to using the training data.

```R
predict(model)
```
