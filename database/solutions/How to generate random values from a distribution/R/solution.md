---
author: Nathan Carter (ncarter@bentley.edu)
---

Because R is designed for use in statistics,
it comes with many probability distributions built in.
A list of them is online [here](https://cran.r-project.org/doc/manuals/r-release/R-intro.html#Probability-distributions).

Regardless of whether the distribution is discrete or continuous,
prefix the name of the distribution with `r`, which stands for "random values."
Here are two examples.

Using a **normal distribution:**

```python
# 20 random values from the normal distribution with μ=10 and σ=5
rnorm( 20, mean=10, sd=5 )
```

Using a **uniform distribution:**

```python
# 20 random values from the uniform distribution on the interval [50,60]
runif( 20, min=50, max=60 )
```
