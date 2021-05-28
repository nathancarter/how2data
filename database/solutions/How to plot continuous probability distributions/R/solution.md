---
author: Nathan Carter (ncarter@bentley.edu)
---

Because R is designed for use in statistics,
it comes with many probability distributions built in.
A list of them is online [here](https://cran.r-project.org/doc/manuals/r-release/R-intro.html#Probability-distributions).

The challenge with plotting a random variable is knowing the appropriate
sample space, because some random variables have sample spaces of infinite
width, which cannot be plotted.

But we can just ask R to show us the central 99.98% of a continuous
distribution, which is almost always indistinguishable
to the human eye from the entire distribution.

We will use a normal distribution with $\mu=10$ and $\sigma=5$,
but if you wanted to use a different distribution,
you could replace `qnorm` and `dnorm` with, for example,
`qchisq` and `dchisq` (for the $\chi^2$ distribution),
adjusting the named parameters as appropriate.
(For a list of supported distributions, see the link above.)

We style the plot below so that it is clear the sample space is continuous.

```R
xmin <- qnorm( 0.0001, mean=10, sd=5 )  # compute min x as the 0.0001 quantile
xmax <- qnorm( 0.9999, mean=10, sd=5 )  # compute max x as the 0.9999 quantile
xs <- seq( xmin, xmax, length.out=100 ) # create 100 values in that range
ys <- dnorm( xs, mean=10, sd=5 )        # compute the shape of the distribution
plot( xs, ys, type='l' )                # plot that shape as a smooth line
```
