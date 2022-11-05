---
author: Nathan Carter (ncarter@bentley.edu)
---

We assume you have already fit a linear model to the data,
as in the code below, which is explained fully in a separate task,
how to fit a linear model to two columns of data.

```julia
using GLM, DataFrames
xs = [ 393, 453, 553, 679, 729, 748, 817 ]
ys = [  24,  25,  27,  36,  55,  68,  84 ]
data = DataFrame( xs=xs, ys=ys )
model = lm( @formula( ys ~ xs ), data )
```

You can get the $R^2$ value from your model using the `r2` function in the GLM package.

```julia
r2( model )
```
