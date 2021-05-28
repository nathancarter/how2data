---
author: Nathan Carter (ncarter@bentley.edu)
---

R expects you to have all the samples in one vector,
and the groups they came from in a separate, categorical vector.
So, for example, if we had SAT scores from four different schools
(named A, B, C, and D), then our data might be arranged like this.

```R
SAT.scores <- c(
    1100, 1250, 1390, 970, 1510, 1010, 1050, 1090, 1110,
    900, 1550, 1300, 1270, 1210, 900, 850, 1110, 1070, 910, 920
)
school.names <- c(
    'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B',
    'C', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'D', 'D'
)
```

ANOVA tests the null hypothesis that all group means are equal.
You choose $\alpha$, the probability of Type I error
(false positive, finding we should reject $H_0$ when it's actually true).
I will use $\alpha=0.05$ in this example.

```R
# Run a one-way ANOVA and print a summary of all the output
result <- aov( SAT.scores ~ school.names )
summary( result )
```

The $p$-value reported in that output is $0.0433$.
You could manually check whether $p<\alpha$.
Since it is, we would reject $H_0$, and therefore conclude
that at least one pair of means is statistically significantly different.

Or you could ask R to do the comparison for you, but getting the $p$-value
from the ANOVA summary is fiddly:

```R
alpha <- 0.05
p.value <- unname( unlist( summary( result ) ) )[9]
p.value < alpha
```
