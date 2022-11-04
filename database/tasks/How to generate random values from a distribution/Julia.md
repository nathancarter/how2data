---
author: Nathan Carter (ncarter@bentley.edu)
---

You can import many different random variables from Julia's `Distributions` package.
The full list of them is online [here](https://juliastats.org/Distributions.jl/stable/univariate/).

If you don't have that package installed, first run `using Pkg` and then
`Pkg.add( "Distributions" )` from within Julia.

Regardless of whether the distribution is discrete or continuous,
the appropriate function to call is `rand`.
Here are two examples.

Using a **normal distribution:**

```julia
using Distributions
X = Normal( 5, 3 )
rand( X, 10 )
```

Using a **uniform distribution:**

In this example, we generate the random values in one line of code,
without giving the random variable a name.

```julia
using Distributions
rand( Uniform( 100, 200 ), 5 )
```
