---
author: Nathan Carter (ncarter@bentley.edu)
---

We first load a famous dataset, Fisher's irises, just to have some example data to use in the code that follows.  (See how to quickly load some sample data.)


```julia
using RDatasets
iris = dataset( "datasets", "iris" );
```

How big is the dataset?  The output shows number of rows then number of columns.

```julia
size( iris )
```

What are the columns and their data types?  The following command shows the first 5 rows,
plus the column names and types.

```julia
first( iris, 5 )
```

Are any values missing?  The following command answers that question, plus provides
summary statistics, and the same data type information from above.

```julia
describe( iris )
```

The individual statistics are the column headings, and the numeric columns from the original dataset are listed under the "Symbol" heading.

We can also compute these statistics (and others) one at a time for any given set of data points.  Here, we let `xs` be one column from the above DataFrame, but you could use any array or DataFrame instead.

~~~julia
xs = iris."SepalLength"

using Statistics

mean( xs )            # mean, or average, or center of mass
median( xs )          # 50th percentile
quantile!( xs, 0.25 ) # compute any percentile, such as the 25th
var( xs )             # variance
std( xs )             # standard deviation, the square root of the variance
sort( xs )            # data in increasing order
sum( xs )             # sum, or total
~~~
