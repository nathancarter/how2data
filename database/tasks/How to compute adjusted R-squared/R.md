---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We assume you have already fit a multiple linear regression model to the data, as in the code below.
(If you're unfamiliar with how to do so, see how to fit a multiple linear regression model.)
The data shown below is fake, and we assume you will replace it with your own real data if you use this code.

```R
x1 <- c(2, 7, 4, 3, 11, 18, 6, 15, 9, 12)
x2 <- c(4, 6, 10, 1, 18, 11, 8, 20, 16, 13)
x3 <- c(11, 16, 20, 6, 14, 8, 5, 23, 13, 10)
y <- c(24, 60, 32, 29, 90, 45, 130, 76, 100, 120)
model <- lm(y ~ x1 + x2 + x3)
```

You can get a lot of information about your model from its summary.

```R
summary(model)
```

In particular, that printout contains the Adjusted $R^2$ value; it is the second value in the right-hand column, near the top.

You can also obtain it directly, as follows:

```R
summary(model)$adj.r.squared
```

In this case, the Adjusted $R^2$ is $0.3904$.
