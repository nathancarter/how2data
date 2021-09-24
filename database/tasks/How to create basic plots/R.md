---
author:
 - Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
 - Nathan Carter (ncarter@bentley.edu)
---

We will create some fake data using vectors, for simplicity. But everything we show below works also if your data is in columns of a DataFrame.

```R
patient.id     <- c(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
patient.height <- c(60,  64,  64,  65,  66,  66,  70,  72,  72,  76)
patient.weight <- c(141, 182, 169, 204, 138, 198, 180, 175, 244, 196)
```

We can make a line plot if we use the `type="l"` option (which is an "ell," not a number one).

```R
plot(patient.id, patient.height, main="Patient heights", type="l")
```

We can create a scatterplot if we have two numerical columns, such as the height and weight in the data above.

```R
plot(patient.height, patient.weight, main = "Height vs. Weight")
```
