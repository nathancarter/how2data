---
author: Nathan Carter (ncarter@bentley.edu)
---

We use the `power.t.test` function in R.  It embodies a relationship among
five variables; you provide any four of them and it will compute the fifth to
be consistent with the first four, regarding the two-sample $t$-test you plan

For this example, let's say that:

 * You plan to create a balanced $4\times2$ factorial experiment with 32 subjects.
 * You wish to be able to detect a difference 
 * You want to know the expected power for the test of a main effect of factor A.
 * Your significance level is $\alpha=0.05$.

We proceed as follows.

```R
# install.packages('pwr') # if you have not already installed it
library(pwr)

obs <- 32       # number of subjects (or observations)
effect <- 0.25  # effect size 
alpha <- 0.05   # significance level
ratio <- 1      # ratio of the number of observations in one sample to the other

# We leave power unspecified, so that power.t2n.test will compute it for us:
pwr.t2n.test(n1=obs, n2=obs, d=effect, sig.level=alpha, power=NULL)
```

The power is 0.1663, which means that the probability of rejecting the null hypothesis when in fact it is false OR the probability of avoiding a Type II error is 0.1663.
