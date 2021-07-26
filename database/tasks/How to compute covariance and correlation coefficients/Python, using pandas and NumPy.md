---
author: Nathan Carter (ncarter@bentley.edu)
---

We will construct some random data here, but when applying this, you would use your own data, of course.

```python
import pandas as pd
import numpy as np
df = pd.DataFrame(np.random.rand(10,5))
df.columns = [ 'col1','col2','col3','col4','col5' ]
df.head()
```

If you have two pandas Series, you can compute the covariance of just those two variables.  Note that every column in a DataFrame is a pandas series.

```python
np.cov( df['col1'], df['col2'] )
```

You can also compare all of a DataFrame's columns among one another, each as a separate variable.

```python
df.cov()
```

The Pearson correlation coefficient can be computed with `np.corrcoef` in place of `np.cov`.

```python
np.corrcoef( df['col1'], df['col2'] )
```

And pandas DataFrames have a built in method to do this for all numeric columns.

```python
df.corr()
```

