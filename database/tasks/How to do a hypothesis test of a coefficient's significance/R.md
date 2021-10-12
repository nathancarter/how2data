---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We will use the fake data shown below with a single variable model.
You can use a model created from your own actual data instead.

```R
x <- c( 34,   9,  78,  60,  22,  45,  83,  59,  25)
y <- c(126, 347, 298, 309, 450, 187, 266, 385, 400)
model <- lm(y ~ x)
```

We can test whether a coefficient is zero by using that as our null hypothesis,
$H_0: \beta_i = 0$. We can use any value $0 \le \alpha \le 1$ as our Type 1 error
rate; we will set $\alpha$ to be 0.05 here.

The answer to our hypothesis test can be obtained by looking at just the
coefficients portion of the model summary:

```R
summary(model)$coef
```

The final column of output shows $p$-values for each $\beta_i$.  The $p$-value
associated with the $x$ row is therefore for $\beta_1$, the coefficient on $x$.
Because it is 0.515358250, which is greater than $\alpha$, we cannot reject the
null hypothesis, and we should continue to assume that $\beta_1=0$ and there is
no significant relationship between the explanatory and response variable in
this situation.
