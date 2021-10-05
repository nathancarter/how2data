---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We'll assume that you already have a linear model in multiple variables.
This is the unrestricted model, in the sense that it includes all the variables.
We create an example below using fake data.

```R
x1 <- c(2, 7, 4, 3, 11, 18, 6, 15, 9, 12)         # Independent variables
x2 <- c(4, 6, 10, 1, 18, 11, 8, 20, 16, 13)
x3 <- c(11, 16, 20, 6, 14, 8, 5, 23, 13, 10)
y <- c(24, 60, 32, 29, 90, 45, 130, 76, 100, 120) # Dependent variable
model.unrestricted <- lm(y ~ x1 + x2 + x3)        # Unrestricted model
```

As an example, we will test whether $\beta_2$ and $\beta_3$ are jointly equal to
zero, that is, our null hypothesis will be $H_0: \beta_2 = \beta_3 = 0$.
If $H_0$ is true, that would lead to a smaller model, called the restricted
model, that does not include those two terms.

```R
model.restricted <- lm(y ~ x1)                    # Restricted model
```

We choose a value $0 \le \alpha \le 1$ as our Type 1 error rate.
Let's set $\alpha$ to be 0.05 here.

The formula for the F-statistic requires a few basic facts about our situation,
such as the size of the data set and the models.  Note that when counting terms
in a model, we must include the intercept terms as well.

```R
n <- length(y)      # number of observations
k <- 4              # number of coefficients in unrestricted model
p <- 2              # number of terms removed to make restricted model
```

The formula for the F-statistic also requires the sum of squared errors
(SSE) for both models, which R can compute for us.

```R
SSE.unrestricted <- sum((fitted(model.unrestricted) - y)^2)
SSE.restricted <- sum((fitted(model.restricted) - y)^2)
```

The test statistic is then computed and evaluated against our chosen $\alpha$
as follows.

```R
f.statistic <- ( ((SSE.restricted - SSE.unrestricted) / p)
               / (SSE.unrestricted / (n-k)) )            # F-statistic
pf(f.statistic, df1 = p, df2 = n-k, lower.tail = FALSE)  # p-value
```

Our $p$-value is greater than $\alpha$, so we cannot reject the null hypothesis.
In this case, we cannot reject the null hypothesis, so we should proceed as if
$\beta_2=\beta_3=0$ and choose to use the restricted model.
