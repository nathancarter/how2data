---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We're going to use fake data here for illustrative purposes. You can replace our fake data with your real data in the code below.

```R
# Replace this fake data with your real data
x1 <- c(2, 7, 4, 3, 11, 18, 6, 15, 9, 12)
x2 <- c(4, 6, 10, 1, 18, 11, 8, 20, 16, 13)
x3 <- c(11, 16, 20, 6, 14, 8, 5, 23, 13, 10)
y <- c(24, 60, 32, 29, 90, 45, 130, 76, 100, 120)

# If you'll need the model coefficients later, store them as variables like this:
model <- lm(y ~ x1 + x2 + x3)
beta0 <- model$coefficients[1]
beta1 <- model$coefficients[2]
beta2 <- model$coefficients[3]
beta3 <- model$coefficients[4]

# To see the model summary, which includes the coefficients and much more, do this:
summary(model)
```

The coefficients and intercept appear on the left hand side of the output, about half way down, under the heading "Estimate."

Thus the multiple linear regression model from the example data is $\hat y = 77.244 - 2.701x_1  +  7.299x_2  - 4.861x_3$.
