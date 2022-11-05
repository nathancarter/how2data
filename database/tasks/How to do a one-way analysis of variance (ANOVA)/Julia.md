---
author: Nathan Carter (ncarter@bentley.edu)
---

Let's assume we have our samples in several different Julia arrays.
Here I'll construct some made-up data about SAT scores at four different
schools.

```julia
school1_SATs = [ 1100, 1250, 1390, 970, 1510 ];
school2_SATs = [ 1010, 1050, 1090, 1110 ];
school3_SATs = [ 900, 1550, 1300, 1270, 1210 ];
school4_SATs = [ 900, 850, 1110, 1070, 910, 920 ];
```

ANOVA tests the null hypothesis that all group means are equal.
You choose $\alpha$, the probability of Type I error
(false positive, finding we should reject $H_0$ when it's actually true).
I will use $\alpha=0.05$ in this example.

```julia
using HypothesisTests
alpha = 0.05
p_value = pvalue( OneWayANOVATest( school1_SATs, school2_SATs, school3_SATs, school4_SATs ) )
reject_H0 = p_value < alpha
alpha, p_value, reject_H0
```

The result we see above is to reject $H_0$, and therefore conclude
that at least one pair of means is statistically significantly different.

If you are using the most common $\alpha$ value of $0.05$, you can save a few lines of code
and get a more detailed printout by just printing out the test itself:

```julia
OneWayANOVATest( school1_SATs, school2_SATs, school3_SATs, school4_SATs )
```
