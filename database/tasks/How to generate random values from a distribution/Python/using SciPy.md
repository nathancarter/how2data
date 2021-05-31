---
author: Nathan Carter (ncarter@bentley.edu)
---

You can import many different random variables from SciPy's `stats` module.
The full list of them is online [here](https://docs.scipy.org/doc/scipy/reference/stats.html#discrete-distributions).

Regardless of whether the distribution is discrete or continuous,
the appropriate function to call is `rvs`, which stands for "random values."
Here are two examples.

Using a **normal distribution:**

```python
from scipy import stats
X = stats.norm( 10, 5 )  # normal random variable with μ=10 and σ=5
X.rvs( 20 )              # 20 random values from X
```

Using a **uniform distribution:**

(Note that in SciPy, the uniform distribution needs a "location,"
which is where the sample space begins---in this case 50---and a "scale,"
which is the width of the sample space---in this case 10.)

```python
from scipy import stats
X = stats.uniform( 50, 10 )  # uniform random variable on the interval [50,60]
X.rvs( 20 )                  # 20 random values from X
```
