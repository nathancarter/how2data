---
author:
 - Nathan Carter (ncarter@bentley.edu)
 - Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

Because R is designed for use in statistics,
it comes with many probability distributions built in.
A list of them is online [here](https://cran.r-project.org/doc/manuals/r-release/R-intro.html#Probability-distributions).

To compute a probability from a **discrete** distribution, prefix the name
of the distribution with `d` (for "density") and call it as a function on the
value whose probability you want to know, plus any parameters the distrubtion needs.

```R
# For a binomial random variable with 10 trials
# and probability 0.5 of success on each trial,
# what is the probability of exactly 3 successes?
dbinom( 3, size=10, prob=0.5 )
```

If you change the prefix to `p`, then R will compute the probability *up to*
the parameter you specify, as in the following example.

```R
# For a binomial random variable with 10 trials
# and probability 0.5 of success on each trial,
# what is the probability of up to (and including) 3 successes?
pbinom( 3, size=10, prob=0.5 )
```

To compute a probability from a **continuous** distribution, prefix the
name with `d`, just as in the example above.  But you can compute only
the probability that a random value will fall in an interval $[a,b]$,
not the probability that it will equal a specific value.

```R
# For a normal random variable with mean μ=10 and standard deviation σ=5,
# what is the probability of the value lying in the interval [12,13]?
pnorm( 13, mean=10, sd=5 ) - pnorm( 12, mean=10, sd=5 )
```

Consequently, we can also compute:

```R
pnorm( 13, mean=10, sd=5 )     # the probability of a value < 13
1 - pnorm( 13, mean=10, sd=5 ) # the probability of a value > 13
```
