---
author:
 - Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
 - Krtin Juneja (KJUNEJA@falcon.bentley.edu)
---

The solution below uses an example dataset about car design and fuel consumption from a 1974 Motor Trend magazine. (See how to quickly load some sample data.)

```R
# install.packages("datasets") # if you have not done so already
library(datasets)
data(mtcars)
df <- mtcars
```

Consider a model using number of cylinders (cyl) and weight of car (wt) to predict its fuel efficiency (mpg). We create this model and perform an ANOVA to see if the predictors are significant.

```R
# Build the model
add_model <- lm(mpg ~ cyl + wt, data = df)
# Perform an ANOVA
anova(add_model)
```

The final column of output suggests that both predictors are significant. But do the two predictors have an interaction effect? Let’s create a model containing the interaction term.

```R
# Build the model with interaction
int_model <- lm(mpg ~ cyl * wt, data = df)
# Perform an ANOVA
anova(int_model)
```

As seen in the final column of output, there is a significant interaction between the two predictors. To check which model is better, we can conduct an ANOVA comparing the two models.

```R
# Use ANOVA to compare the models
anova(add_model, int_model)
```

We have just performed this hypothesis test:

$H_0 =$ the two models are equally as useful for predicting the outcome

$H_a =$ the larger model is significantly better than the smaller model

The one number in the final column is our test statistic.  Since is below our chosen threshold of $0.05$, it is best to use the second model.

This method can be used to check if covariates should be included in the model, or if additional variables should be added as well.
