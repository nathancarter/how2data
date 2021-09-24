---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

For the purposes of this example, let's say we have a sample of GPAs from
matriculated students at three Ivy League institutions:
Harvard, Dartmouth, and Columbia. This is example data, and you can replace it
with your actual data when you re-use this code.

R requires that our categories and our numeric sample values be in separate vectors.
We could structure our data as follows.

```R
gpas <- c( 3.40, 3.66, 3.90, 3.55, 3.90, 3.58,
           3.90, 3.97, 3.92, 3.83, 4.00, 3.68,
           4.00, 3.75, 3.34 )
schools <- c(
    "Harvard", "Harvard", "Harvard", "Harvard", "Harvard", "Harvard",
    "Dartmouth", "Dartmouth", "Dartmouth", "Dartmouth", "Dartmouth", "Dartmouth",
    "Columbia", "Columbia", "Columbia" )
```

The Kruskal-Willis Test uses a null hypothesis that the category medians are equal,
$H_0: m_C = m_H = m_D \le 0$.
We choose $\alpha$, or the Type I error rate, as 0.05 and run the test as shown below.

```R
kruskal.test(gpas, schools)
```

The p-value, 0.1568, is greater than $\alpha$, so we fail to reject the null hypothesis.
We do not have sufficient evidence to conclude that the median GPAs
of matriculated students at these three schools are different from each other.
