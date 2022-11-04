---
author: Nathan Carter (ncarter@bentley.edu)
---

If we choose a value $0 \le \alpha \le 1$ as our Type 1 error rate,
then we can find the critical value from the normal distribution using the
`quantile()` function in Julia's Distributions package.

If you don't have that package installed, first run `using Pkg` and then
`Pkg.add( "Distributions" )` from within Julia.

The code below shows how to do this for left-tailed,
right-tailed, and two-tailed hypothesis tests.

```julia
using Distributions
alpha = 0.05                  # Replace with your alpha value
n = 68                        # Replace with your sample size
tdist = TDist( n - 1 )
quantile( tdist, alpha )      # Critical value for a left-tailed test
```

```julia
quantile( tdist, 1 - alpha )  # Critical value for a right-tailed test
```

```julia
quantile( tdist, alpha / 2 )  # Critical value for a two-tailed test
```

We can also compute $p$-values from the normal distribution to compare to a
test statistic.  As an example, we'll use a test statistic of 2.67, but you can
substitute your test statistic's value instead.

We can find the $p$-value for this test statistic using the `cdf()` function
in Julia's Distributions package.
Again, we show code for left-tailed, right-tailed, and two-tailed tests.

```julia
test_statistic = 2.67                     # Replace with your test statistic
cdf( tdist, test_statistic )              # p-value for a left-tailed test
```

```julia
1 - cdf( tdist, test_statistic )          # p-value for a right-tailed test
```

```julia
2 * ( 1 - cdf( tdist, test_statistic ) )  # p-value for a two-tailed test
```