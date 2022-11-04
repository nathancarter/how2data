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

The example below uses a geometric distribution, whose sample space is
$\{1,2,3,\ldots\}$.  We specify that we just want to use $x$ values
in the set $\{1,2,\ldots,10\}$.  (In some software, the geometric
distribution's sample space begins at 0, but not in SciPy.)

We style the plot below so that it is clear the sample space is discrete.

```julia
using Distributions
X = Geometric( 0.5 )      # use a geometric distribution with p=0.5
xs = 1:10                 # specify the range to be 1,2,3,...,10

using Plots
bar( xs, pdf.( X, xs ) )  # plot the shape of the distribution
```
