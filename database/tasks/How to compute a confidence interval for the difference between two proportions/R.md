---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

Here is some fake data for the purposes of this illustration. Let's say we conduct a survey of people in Boston and of people in Nashville and ask them if they prefer chocolate or vanilla ice cream. We want to compare the proportions of people from the two cities who like vanilla.

 * Out of 150 people in Boston surveyed, 90 prefer vanilla.
 * Out of 135 people in Nashville surveyed, 50 prefer vanilla.

We'll let $\bar{p_1}$ represent the proportion of people from Boston who like vanilla and $\bar{p_2}$ represent the proportion of people from Nashville who like vanilla. You can replace the code for this fake data below with your real data. 

```R
# number of observations in the samples
n1 <- 150
n2 <- 135
# proportions in the two samples
p_bar1 <- 90/150
p_bar2 <- 50/135
```

We now compute the confidence interval using R's `qnorm` function.

```R
# Find the critical value to compute the confidence interval
alpha <- 0.05       # replace with your chosen alpha (here, a 95% confidence level)
critical_value <- qnorm(p = alpha/2, lower.tail=FALSE)

# Compute the standard error of the proportions
std_error <- sqrt( p_bar1*(1-p_bar1)/n1 + p_bar2*(1-p_bar2)/n2 )

# Compute the upper and lower bounds of the confidence interval and print them out
upper_bound <- (p_bar1 - p_bar2) + critical_value*std_error
lower_bound <- (p_bar1 - p_bar2) - critical_value*std_error
lower_bound
upper_bound
```

The confidence interval for the difference between these two proportions is $[0.11657, 0.34269]$.
