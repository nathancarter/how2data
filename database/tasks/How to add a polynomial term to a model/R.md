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

Let's model temperature as the dependent variable with pressure squared as the
independent variable.  To place the "pressure squared" term in the model, we use
R's `poly` function, as shown below.  It automatically includes a pressure term
as well (not squared).

```R
# Build the model
model <- lm(temperature ~ poly(pressure, 2), data = pressure)
summary(model)
```

Now we have a model of the form $\hat t = 180 + 361.84p - 186.66p^2$,
where $t$ stands for temperature and $p$ for pressure.

You can change the number in the `poly` function.
For example, if we wanted to create a third-degree polynomial term
then we would have specified `poly(pressure, 3)`, and it would have included pressure,
pressure squared, and pressure cubed.
