---
author: Nathan Carter (ncarter@bentley.edu)
---

Let's create a small example DataFrame to use here (using the method from
how to create a data frame from scratch).
Naturally, you would apply this solution to your own data instead.

```python
import pandas as pd
df = pd.DataFrame( { 'Date' : [ '5/7/19', '5/10/19', '5/11/19' ],
                     'Event' : [ 'Work', 'Party', 'More work' ] } )
df
```

If you've already got the data in a DataFrame column, and you wish to convert it to dates, use the `pd.to_datetime` function, which will do its best to read whatever format your dates are in:

```python
df['Date'] = pd.to_datetime( df['Date'] )
df
```

But if they aren't in a standard format, you can specify just about any format as in the following example.  [See the Python documentation](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) for format details.

~~~python
# If the dates had been, for example, 5-7-2019 10:15:00
df['Date'] = pd.to_datetime( df['Date'], format="%m-%d-%Y %H:%M:%S" )
~~~

It's often easier to handle date conversions while reading the data.  You can tell pandas to read dates in most of the common date formats using any of the following methods.

~~~python
# Any columns that look like dates, treat as dates:
df = pd.read_csv( "example.csv", parse_dates=True )

# Convert the specific columns you name into dates:
df = pd.read_csv( "example.csv", parse_dates=['col1','col2'] )

# If the date is spread over multiple columns, do this:
# (Let's say the year, month, and day are in columns, 4, 5, and 6.)
df = pd.read_csv( "example.csv", parse_dates=[[4,5,6]] )
# Note the double brackets, and indices start counting at zero.
~~~

