---
author: Nathan Carter (ncarter@bentley.edu)
---

You can import many different random variables from SciPy's `stats` module.
The full list of them is online [here](https://docs.scipy.org/doc/scipy/reference/stats.html#discrete-distributions).

To compute a probability from a **discrete** distribution, create a random
variable, then use its Probability Mass Function, `pmf`.

```python
from scipy import stats

# Create a binomial random variable with 10 trials
# and probability 0.5 of success on each trial
X = stats.binom( 10, 0.5 )

# What is the probability of exactly 3 successes?
X.pmf( 3 )
```

To compute a probability from a **continuous** distribution, create a random
variable, then use its Cumulative Density Function, `cdf`.  You can only
compute the probability that a random value will fall in an interval $[a,b]$,
not the probability that it will equal a specific value.

```python
from scipy import stats

# Create a normal random variable with mean μ=10 and standard deviation σ=5
X = stats.norm( 10, 5 )

# What is the probability of the value lying in the interval [12,13]?
X.cdf( 13 ) - X.cdf( 12 )
```
