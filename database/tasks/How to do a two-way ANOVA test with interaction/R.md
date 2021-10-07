---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We're going to use R's `esoph` dataset, about esophageal cancer cases.
We will focus on the impact of age group (`agegp`) and alcohol consumption (`alcgp`)
on the number of cases of the cancer (`ncases`).  We ask, does the interaction
between these two factors affect the number of cases?

First, we load in the dataset.  (See how to quickly load some sample data.)

```R
# install.packages("datasets") # if you have not already done this
library(datasets)
data <- esoph
head(data)
```

Next, we create a model that includes the response variable we care about,
plus the two categorical variables we will be testing, as well as their
interaction term.

```R
# the * below means multiplication, to create an interaction term
model <- aov(ncases ~ agegp*alcgp, data = data)
```

A two-way ANOVA with interaction tests the following three null hypotheses.

 1. There is no interaction between the two categorical variables.
    (If we reject this we do not test the other two hypotheses.)
 2. The mean response is the same across all groups of the first factor.
    (In our example, that says the mean `ncases` is the same for all age groups.)
 3. The mean response is the same across all groups of the second factor.
    (In our example, that says the mean `ncases` is the same for all alcohol consumption groups.)

We choose a value, $0 \le \alpha \le 1$, as the Type I Error Rate. Let's let $\alpha=0.05$ here.

```R
summary(model)
```

The $p$-value for the interaction of age group and alcohol consumption is in
the third row, final column, $0.03633$.  It is less than $\alpha$,
so we can reject the null hypothesis that age group and alcohol consumption
do not interact with regards to the number of esophageal cancer cases.  That is,
we have reason to believe that their interaction does effect the outcome.

As we stated when we listed the hypotheses to test, since we rejected the first
null hypothesis, we will not test the other two.  In the case where you failed
to reject the first null hypothesis, you could consider each $p$-value in the
first two rows of the above table, one for each of the two factors.
