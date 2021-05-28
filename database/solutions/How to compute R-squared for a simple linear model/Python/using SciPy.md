---
author: Nathan Carter (ncarter@bentley.edu)
---

We assume you have already fit a linear model to the data,
as in the code below, which is explained fully in a separate task,
How to fit a linear model to two columns of data.

```python
import scipy.stats as stats
xs = [ 393, 453, 553, 679, 729, 748, 817 ]
ys = [  24,  25,  27,  36,  55,  68,  84 ]
model = stats.linregress( xs, ys )
```

The $R$ value is part of the model object that `stats.linregress` returns.

```python
model.rvalue
```

You can compute $R^2$ just by squaring it.

```python
model.rvalue ** 2
```
