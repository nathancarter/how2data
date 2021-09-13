---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

Let's assume that you've already built a linear model similar to the one below.
This one uses a small amount of fake data, but it's just an example.

```R
xs <- c( 393, 453, 553, 679, 729, 748, 817 )
ys <- c(  24,  25,  27,  36,  55,  68,  84 )
model <- lm(ys ~ xs)
```

We can extract the residuals of the model in either of two ways.

R has a built-in `residuals()` function for this purpose.

```R
residuals(model)
```

The model itself has a `$residuals` attribute.

```R
model$residuals
```
