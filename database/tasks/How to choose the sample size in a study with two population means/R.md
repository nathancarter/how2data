---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

Example:  Let's say we're designing a study to assess the effectiveness of a new
four-week exercise program for weight loss.  Assume that weight loss in four-week
exercise programs is normally distributed with a standard deviation of around 5 pounds.
The goal is that the new exercise program will have a 4-pound higher weight loss
than the average program.  (Notice that we will be comparing the means of two
populations, the weight loss in each of two programs.)

We choose a value $0 \le \alpha \le 1$ as the probability of a Type I error
in our test that compares the two means.  (Recall, Type I error is for a
false positive, finding we should reject $H_0$ when it’s actually true).
Let's set $\alpha$ to be 0.05 here.

We choose a value $0 \le \beta \le 1$ as the probability of a Type II error
(false negative, failing to reject $H_0$ when it’s actually false).
Let's set $\beta$ to be 0.2 here.  The test's power is $1-\beta$, or in this case,
0.8.

What should the sample size be for each group?

```R
# sd = standard deviation = 5 pounds
# delta = desired increase = 4 pounds
# sig.level = alpha = 0.05
# power = 1 - beta = 1 - 0.20 = 0.80
# n = NULL so R computes it for us
power.t.test(n = NULL, delta = 4, sd = 5, sig.level = 0.05, power = 0.80)
```

Our sample size needs to be 26 participants in order for the power of the study
to be 80% with our specified parameters.
