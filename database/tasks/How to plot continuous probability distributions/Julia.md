---
author: Nathan Carter (ncarter@bentley.edu)
---

You can import many different random variables from Julia's `Distributions` package.
The full list of them is online [here](https://juliastats.org/Distributions.jl/stable/univariate/).

If you don't have that package installed, first run `using Pkg` and then
`Pkg.add( "Distributions" )` from within Julia.

The challenge with plotting a random variable is knowing the appropriate
sample space, because some random variables have sample spaces of infinite
width, which cannot be plotted.

But we can just ask Julia to show us the central 99.98% of a continuous
distribution, which is almost always indistinguishable
to the human eye from the entire distribution.

We style the plot below so that it is clear the sample space is continuous.

```julia
using Distributions
X = Normal( 10, 5 )                   # use a normal distribution with μ=10 and σ=5

xmin = quantile( X, 0.0001 )          # compute min x as the 0.0001 quantile
xmax = quantile( X, 0.9999 )          # compute max x as the 0.9999 quantile
xs = range( xmin, xmax, length=100 )  # create 100 x values in that range

using Plots
plot( xs, pdf.( X, xs ) )             # plot the shape of the distribution
```
