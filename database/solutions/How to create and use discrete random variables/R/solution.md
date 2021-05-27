---
author: Nathan Carter (ncarter@bentley.edu)
---

Because R is designed for use in statistics,
it comes with many probability distributions built in.
A list of them is online [here](https://cran.r-project.org/doc/manuals/r-release/R-intro.html#Probability-distributions).
The examples below use the Bernoulli and binomial distributions as examples.

You can **compute the probability** of any given outcome.
If using the binomial distribution, which is called `binom` in R,
we place a `d` on the front to compute discrete probabilities.

```R
# probability of exactly 3 successes in 10 trials, with p=0.25 for each trial
dbinom( 3, size=10, prob=0.25 )
```

You can **generate random values.**  Use the same name (such as `binom`),
but prefix it with `r` to generate random values.  In the example below,
we will generate values from a geometric distribution with probability $p=0.5$.

```R
rgeom( 15, prob=0.5 )  # generate 15 random values
```

You can **plot the distribution** of a discrete random variable.  We will use the
same geometric distribution as in the previous example, but if you wanted to use
a different distribution, you could replace `dgeom` with, for example, `dbinom`,
adjusting the named parameters as appropriate.

Note that you must supply the sample space, because it is not always
possible to compute it; some sample spaces are infinite, and you must
choose which subset of the infinite sample space ($x$ axis) you want to view.

```R
xs = 0:8                     # choose the sample space (here, it's 0,1,2,...,8)
ys = dgeom( xs, prob=0.5 )   # compute the shape of the distribution
plot( xs, ys, type='p',      # plot circles...
      xlab='sample space', ylab='probability' )
segments( xs, 0, xs, ys )    # ...and lines
```
