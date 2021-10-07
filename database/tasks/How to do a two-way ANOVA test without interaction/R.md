---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We're going to use R's `esoph` dataset, about esophageal cancer cases.
We will focus on the impact of age group (`agegp`) and alcohol consumption (`alcgp`)
on the number of cases of the cancer (`ncases`).  We ask, does either of
these two factors affect the number of cases?

First, we load in the dataset.  (See how to quickly load some sample data.)

```R
# install.packages("datasets") # if you have not already done this
library(datasets)
data <- esoph
head(data)
```

Next, we create a model that includes the response variable we care about,
plus the two categorical variables we will be testing.
We simply omit the interaction term.  (If you wish to include it, see
how to do a two-way ANOVA test with interaction.)

```R
# the * below means multiplication, to create an interaction term
model <- aov(ncases ~ agegp + alcgp, data = data)
```

A two-way ANOVA with interaction tests the following two null hypotheses.

 1. The mean response is the same across all groups of the first factor.
    (In our example, that says the mean `ncases` is the same for all age groups.)
 2. The mean response is the same across all groups of the second factor.
    (In our example, that says the mean `ncases` is the same for all alcohol consumption groups.)

We choose a value, $0 \le \alpha \le 1$, as the Type I Error Rate. Let's let $\alpha=0.05$ here.

```R
summary(model)
```

The $p$-value for the alcohol consumption factor is in the first row, final column, $1.029452\times10^{-2}$.
It is less than $\alpha$, so we can reject the null hypothesis that alcohol consumption
does not affect the number of esophageal cancer cases.  That is, we have reason to
believe that it does affect the number of cases.

The $p$-value for the age group factor is in the second row, final column, $8.907998\times10^{-9}$.
It is less than $\alpha$, so we can reject the null hypothesis that age group
does not affect the number of esophageal cancer cases.  Again, we have reason to
believe that it does affect the number of cases.
