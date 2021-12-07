---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

Let's assume that you already made your multiple regression model, similar to the one shown below. You can visit this task, , to see how to construct a multivariate linear model.

Let's assume that you already made your multivariate linear model,
similar to the one shown below. If you still need to create one, first see
how to fit a multivariate linear model.

We use example data here, but you would use your own data instead.

```R
x1 <- c( 2,  7,  4,  3, 11, 18,   6, 15,   9,  12)
x2 <- c( 4,  6, 10,  1, 18, 11,   8, 20,  16,  13)
x3 <- c(11, 16, 20,  6, 14,  8,   5, 23,  13,  10)
y  <- c(24, 60, 32, 29, 90, 45, 130, 76, 100, 120)
model <- lm(y ~ x1 + x2 + x3)
```

Now we want to test whether the model is significant.  We will use a null hypothesis
that states that all of the model's coefficients are equal to zero, that is, they are
not jointly significant in predicting $y$.  We can write $H_0: \beta_0 = \beta_1 = \beta2 = \beta_3 = 0$.

We also choose a value $0 \le \alpha \le 1$ as our Type 1 error rate. Herer we'll use
$\alpha=0.05$.

The summary output for the model will give us both the F-statistic and the p-value.

```R
summary(model)
```

In the final line of the output, we can see that the F-statistic is 2.921.
The corresponding $p$-value in the same line is 0.1222, which is greater than $\alpha$,
so we do not have sufficient evidence to reject the null hypothesis.

We cannot conclude that the independent variables in our model are jointly significant
in predicting the response variable.
