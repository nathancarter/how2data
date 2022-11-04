---
author: Nathan Carter (ncarter@bentley.edu)
---

You can import many different random variables from Julia's `Distributions` package.
The full list of them is online [here](https://juliastats.org/Distributions.jl/stable/univariate/).

If you don't have that package installed, first run `using Pkg` and then
`Pkg.add( "Distributions" )` from within Julia.

To compute a probability from a **discrete** distribution, create a random
variable, then use the `pdf` function.  (This is a slight misnomer, because PDF
stands for Probability Density Function, which is a concept related to continuous random
variables, but it's the function Julia uses.)

```julia
using Distributions

# Create a binomial random variable with 10 trials
# and probability 0.5 of success on each trial
X = Binomial( 10, 0.5 )

# What is the probability of exactly 3 successes?
pdf( X, 3 )
```

To compute a probability from a **continuous** distribution, create a random
variable, then use its Cumulative Density Function, `cdf`.  You can only
compute the probability that a random value will fall in an interval $[a,b]$,
not the probability that it will equal a specific value.

```julia
using Distributions

# Create a normal random variable with mean μ=10 and standard deviation σ=5
X = Normal( 10, 5 )

# What is the probability of the value lying in the interval [12,13]?
cdf( X, 13 ) - cdf( X, 12 )
```
