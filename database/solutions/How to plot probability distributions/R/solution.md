---
author: Nathan Carter (ncarter@bentley.edu)
---

Because R is designed for use in statistics,
it comes with many probability distributions built in.
A list of them is online [here](https://cran.r-project.org/doc/manuals/r-release/R-intro.html#Probability-distributions).

The challenge with plotting a random variable is knowing the appropriate
sample space, because some random variables have sample spaces of infinite
width, which cannot be plotted.  So there are two options.

For a **discrete distribution,** you often want to specify the range.

The example below uses a geometric distribution (with $p=0.5$),
whose sample space is $\{0,1,2,3,\ldots\}$.
We specify that we just want to use $x$ values in the set $\{0,1,2,\ldots,10\}$.
(In some software, the geometric distribution's sample space begins at 1,
but not in R.)

If you wanted to use a different distribution, you could replace `dgeom` with,
for example, `dbinom`, adjusting the named parameters as appropriate.

We style the plot below so that it is clear the sample space is discrete.

```R
xs = 0:8                     # choose the sample space (here, it's 0,1,2,...,10)
ys = dgeom( xs, prob=0.5 )   # compute the shape of the distribution
plot( xs, ys, type='p',      # plot circles...
      xlab='sample space', ylab='probability' )
segments( xs, 0, xs, ys )    # ...and lines
```

For a **continuous distribution,** you can just ask R to show you the
central 99.98% of the distribution, which is almost always indistinguishable
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
