---
author: Nathan Carter (ncarter@bentley.edu)
---

Because R is designed for use in statistics,
it comes with many probability distributions built in.
A list of them is online [here](https://cran.r-project.org/doc/manuals/r-release/R-intro.html#Probability-distributions).

The challenge with plotting a random variable is knowing the appropriate
sample space, because some random variables have sample spaces of infinite
width, which cannot be plotted.

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
