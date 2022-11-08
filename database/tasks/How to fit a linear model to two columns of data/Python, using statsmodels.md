---
author: Nathan Carter (ncarter@bentley.edu)
---

This solution uses fake example data.
When using this code, replace our fake data with your real data.

Although the solution below uses plain Python lists of data, it also works if
the data are stored in NumPy arrays or pandas Series.

```python
# Here is the fake data you should replace with your real data.
xs = [ 393, 453, 553, 679, 729, 748, 817 ]
ys = [  24,  25,  27,  36,  55,  68,  84 ]

# We will use statsmodels to build the model
import statsmodels.api as sm

# statsmodels does not add a constant term to the model unless you request it:
xs = sm.add_constant( xs )

# Fit the model and tell us all about it:
model = sm.OLS( ys, xs ).fit()
model.summary()
```

The linear model in this example is approximately $\hat y=0.1327x-37.3214$.
