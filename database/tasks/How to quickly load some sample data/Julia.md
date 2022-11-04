---
author: Nathan Carter (ncarter@bentley.edu)
---

The R programming language comes with many free datasets built in.  To make these
same datasets available to Julia programmers as well, you can install and import
the `RDatasets` package.

First, ensure that you have it installed, by running the Julia commands `using Pkg`
and then `Pkg.add( "RDatasets" )`.  Then you can get access to many datasets as follows:

```julia
using RDatasets
iris = dataset( "datasets", "iris" )
first( iris, 5 ) # just show the first 5 rows
```

But what datasets are available?  There are many!
You can find a full list in the package itself.

```julia
RDatasets.packages()
```
