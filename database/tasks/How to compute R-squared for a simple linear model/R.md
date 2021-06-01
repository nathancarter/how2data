---
author: Nathan Carter (ncarter@bentley.edu)
---

We assume you have already fit a linear model to the data,
as in the code below, which is explained fully in a separate task,
how to fit a linear model to two columns of data.

```R
xs <- c( 393, 453, 553, 679, 729, 748, 817 )
ys <- c(  24,  25,  27,  36,  55,  68,  84 )
model <- lm( ys ~ xs )
```

You can get a lot of information about your model from its summary.

```R
summary( model )
```

In particular, it contains the $R^2$ value.

```R
summary( model )$r.squared
```
