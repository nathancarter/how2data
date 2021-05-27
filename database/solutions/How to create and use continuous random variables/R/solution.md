---
author: Nathan Carter (ncarter@bentley.edu)
---

Because R is designed for use in statistics,
it comes with many probability distributions built in.
A list of them is online [here](https://cran.r-project.org/doc/manuals/r-release/R-intro.html#Probability-distributions).
The examples below use the normal and uniform distributions as examples.

You can **compute the probability** of any interval in the sample space.
Each random variable comes with a cumulative density function (CDF), and
you can use subtraction to compute the probability on an interval $[a,b]$.
Prefix the distribution with `p` to use its CDF.  In the example below,
we use a the normal distribution with $\mu=10$ and $\sigma=5$.

```R
# probability of being in the interval [12,13]
pnorm( 13, mean=10, sd=5 ) - pnorm( 12, mean=10, sd=5 )
```

You can **generate random values.**  Use the same name (such as `norm`),
but prefix it with `r` to generate random values.  In the example below,
we will generate values from a uniform distribution on the interval $[50,60]$.

```R
runif( 15, min=50, max=60 )  # generate 15 random values
```

You can **plot the distribution** of a continuous random variable.  We will use the
same normal distribution as in the first example, but if you wanted to use
a different distribution, you could replace `qnorm` and `dnorm` with, for example,
`qchisq` and `dchisq` (for the $\chi^2$ distribution),
adjusting the named parameters as appropriate.
(For a list of supported distributions, see the link above.)

Here we plot the middle 99.98% of the distribution, but you can adjust
the numbers to plot less or more.  (We cannot plot all of the distribution,
because some distributions have sample spaces of infinite width.)

```R
# find the lowest and highest x values we will use in our plot
xmin <- qnorm( 0.0001, mean=10, sd=5 )
xmax <- qnorm( 0.9999, mean=10, sd=5 )
# create 100 values in that range
xs <- seq( xmin, xmax, length.out=100 )
# plot the shape of the distribution
plot( xs, dnorm( xs, mean=10, sd=5 ), type='l' )
```
