---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We will create some fake data using vectors, for simplicity. But everything we show below works also if your data is in columns of a DataFrame.

```R
patient_id     <- c(0,   1,   2,   3,   4,   5,   6,   7,   8,   9)
patient_height <- c(60,  64,  64,  65,  66,  66,  70,  72,  72,  76)
patient_weight <- c(141, 182, 169, 204, 138, 198, 180, 175, 244, 196)
```

We can use R's boxplot() function to make the plot.

```R
boxplot(patient_weight)
```

You can show more than one variable’s box plot side-by-side by passing both variables into the boxplot() function.

```R
boxplot(patient_height, patient_weight)
```
