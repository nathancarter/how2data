---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

Let's assume that you already fit the linear model, as shown in the code below.
This one uses a small amount of fake data, but it's just an example.
See also how to fit a linear model to two columns of data.

```R
x <- c(34, 9, 78, 60, 22, 45, 83, 59, 25)
y <- c(126, 347, 298, 309, 450, 187, 266, 385, 400)
model <- lm(y ~ x)
```

The standard error is shown as part of the model summary, reported by R's
built-in `summary` function; see the third line from the bottom.

```R
summary(model)
```

We can also extract just that one value using the code shown below.

```R
summary(model)$sigma
```

The standard error of the estimate is 107.119.
