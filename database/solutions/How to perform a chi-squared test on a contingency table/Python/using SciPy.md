---
author: Nathan Carter (ncarter@bentley.edu)
---

Here we will use nested Python lists to store a contingency table of
education vs. gender, taken from
[Penn State University's online stats review website](https://online.stat.psu.edu/statprogram/reviews/statistical-concepts/chi-square-tests).
You should use your own data, and it can be in Python lists or NumPy arrays
or a pandas DataFrame.

```python
data = [
    # HS  BS  MS  Phd
    [ 60, 54, 46, 41 ], # females
    [ 40, 44, 53, 57 ]  # males
]
```

The $\chi^2$ test's null hypothesis is that the two variables are independent.
We choose a value $0\leq\alpha\leq1$ as the probability of a Type I error
(false positive, finding we should reject $H_0$ when it's actually true).

SciPy's stats package provides a `chi2_contingency` function
that does exactly what we need.

```python
alpha = 0.05  # or choose your own alpha here

from scipy import stats
# Run a chi-squared and print out alpha, the p value,
# and whether the comparison says to reject the null hypothesis.
# (The dof and ex variables are values we don't need here.)
chi2_statistic, p_value, dof, ex = stats.chi2_contingency( data )
reject_H0 = p_value < alpha
alpha, p_value, reject_H0
```

In this case, the samples give us enough evidence to reject the null hypothesis
at the $\alpha=0.05$ level.  The data suggest that the two categorical variables
are not independent.
