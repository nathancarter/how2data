---
author: Nathan Carter (ncarter@bentley.edu)
---

This solution uses fake example data.
When using this code, replace our fake data with your real data.

```julia
# Here is the fake data you should replace with your real data.
xs = [ 393, 453, 553, 679, 729, 748, 817 ]
ys = [  24,  25,  27,  36,  55,  68,  84 ]

# Place the data into a DataFrame, because that's what Julia's modeling tools expect:
using DataFrames
data = DataFrame( xs=xs, ys=ys )  # Or you can name the columns whatever you like

# Create the linear model:
using GLM
lm( @formula( ys ~ xs ), data )
```

The linear model in this example is approximately $y=0.13272x-37.3214$.
