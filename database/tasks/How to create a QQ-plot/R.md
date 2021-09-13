---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We're going to use some fake data here by generating random numbers, but you can replace our fake data with your real data in the code below.

```R
# Replace this with your data, such as a variable or column in a DataFrame
values <- c(4, 90, 85, 49, 34, 23, 17, 10, 20, 59, 100, 112, 46, 10, 4, 39, 24, 77, 63, 23, 67, 109, 70)
```

If the data is normally distributed, then we expect that the QQ plot will show the observed values (black circles) falling very clsoe to the red line (the quantiles for the normal distribution).

```R
# Make a QQ plot for the data
qqnorm(values, pch = 1)
# Add the reference line representing what the data should look like if normally distributed
qqline(values, col = "red", lwd = 2)
```

Our observed values fall pretty close to the reference line.  In this case, we expected that, because we created fake data that was normally distributed.  But for real data, it may not stay so close to the red line.
