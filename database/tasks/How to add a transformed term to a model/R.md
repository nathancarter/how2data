---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We're going to use the `Pressure` dataset in R's `ggplot` library as example data.
It contains observations of pressure and temperature.
You would use your own data instead.

```R
# install.packages( "ggplot2" ) # if you haven't done this already
library(ggplot2)
data("pressure")
```

Let's model temperature as the dependent variable with the logarithm of pressure
as the independent variable.  To place the "log of pressure" term in the model, we use
R's `log` function, as shown below.  It uses the naturarl logarithm (base $e$).

```R
# Build the model
model.log <- lm(temperature ~ log(pressure), data = pressure)
summary(model.log)
```

The model is $\hat t = 153.97 + 23.784\log p$,
where $t$ stands for temperature and $p$ for pressure.

Another example transformation is the square root transformation.  As with `log`,
just apply the `sqrt` function to the appropriate term when defining the model.

```R
# Build the model
model.sqrt <- lm(temperature ~ sqrt(pressure), data = pressure)
summary(model.sqrt)
```

The model is $\hat t = 98.561 + 11.446\sqrt{p}$,
with $t$ and $p$ having the same meanings as above.
