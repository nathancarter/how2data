---
author: Elizabeth Czarniak (CZARNIA_ELIZ@bentley.edu)
---

We will create some random data, but that’s just for demonstration purposes. You can apply the answer below to any data. Simply replace the data variable with your real data (a list, a column of a dataframe, etc.).

```R
data <- rnorm(1000)
```

We can use R's hist() function to create the histogram.

```R
hist(data)
```

The y axis in a histogram is frequency, or the number of occurences. You can change it to probabilities instead.

```R
hist(data, prob = TRUE)
```

You can also choose your own bin boundaries. You might specify the number of bin breaks you want, or you can choose the exact bin breaks that you want.

```R
hist(data, breaks = 8)                # Specify number of bin breaks
hist(data, breaks = c(seq(-5, 5, 1))) # Choose exact bin breaks
```
