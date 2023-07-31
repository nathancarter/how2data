---
layout: page
title: Contributing
permalink: /contributing/
nav_order: 7
---

# Contributing to *How to Data*

By contributing to *How to Data,* you're permitting your work to be used under
the same license as the rest of the site.  See licensing information in the
README of [our GitHub repository](http://www.github.com/nathancarter/how2data/).

## If you have a question about stats/data...

You probably want to be browsing our [Tasks page](../tasks).

If your question isn't there, this site may not be the right place for you.
It's a reference for common questions, not a place to ask individual questions.
We highly recommend the following websites that answer custom/individual
questions.

 * For programming questions: [Stack Overflow](https://stackoverflow.com/)
 * For statistics questions: [Cross Validated](https://stats.stackexchange.com/)
 * For mathematics questions: [Math Stack Exchange](https://math.stackexchange.com/)

## If you found a mistake on our site...

Please tell us!  The best way to do so is to file a new
[issue](https://github.com/nathancarter/how2data/issues) in our source code
repository.

## If you have a suggested improvement...

Great!  You can make the edit yourself, and we'll review it for inclusion.
Here's how:

 1. View whichever solution you'd like to improve.
 2. At the bottom of the page, click the link that says "edit the source."
 3. Click the pencil icon on the right above the page content to start editing.
 4. Under the "Commit changes" heading, write a short phrase to explain what
    you're submitting, such as "Fixing incorrect RMSE formula."
 5. Make sure you're creating a new branch and a pull request. (A "pull
    request" is a request for the *How to Data* maintainers to review and
    accept your submission.)
 6. Click "Commit changes."

## If you want to add a new topic...

Excellent!  The [current list of topics](../topics) focuses on courses at
Bentley University, where this website began.  But we'd love to support your institution
as well!  Since the first few courses in statistics and data science include much of
the same material across institutions, the website probably already contains most of the
[tasks](../tasks) (and their solutions!) that you need.  Feel free to reach out directly
[to the site maintainer by email](mailto:ncarter@bentley.edu) and he can easily help you
add a new topic to the site just through an email conversation.

## If you want to create new tasks or solutions...

Excellent!  [The wiki on our GitHub page](https://github.com/nathancarter/how2data/wiki)
will tell you everything you need to know about getting started as a How to Data
developer, whether you're planning a small contribution (like one new solution)
or have big plans (like improving the website build process itself).
We're happy to help you get on board!

## If you're looking for which contributions would be most valuable...

Here's a list!  We would love to have the following new content added to this site,
using any of the methods described above.

 * If you want to translate existing solutions into another language, the site
   automatically generates lists of tasks that need translating.
    * [Tasks with no Python solution yet](software-package-python#solutions-needed-in-python)
    * [Tasks with no R solution yet](software-package-r#solutions-needed-in-r)
    * [Tasks with no Excel solution yet](software-package-excel#solutions-needed-in-excel)<br/>
      (Not every task is feasible in Excel, because some tasks are more advanced statistics than
      can easily be done in Excel, but we are just beginning to have Excel support on the site,
      so there is plenty left to do.)
    * [Tasks with no Julia solution yet](software-package-julia#solutions-needed-in-julia)<br/>
      (We are just beginning to support Julia, so there are many such opportunities.)
 * Basic stats content in Python (such as [what's listed here](bentley-university-gr521))
   typically uses a statistical package like SciPy, but often a smaller library like NumPy
   is sufficient.  Add solutions in Python using just NumPy when possible.
 * For tasks that deal with linear models, some students prefer the Python package
   `statsmodels` and others prefer `sklearn`, because each has different strengths.
   Browse the [full task list](tasks) for tasks that are solved using just one of these packages,
   and add a solution in the other package as well.
 * Intro data science content
    * Create and solve a task, "How to find the data type of a variable or other expression"
    * Create and solve a task, "How to work with lists, arrays, or vectors" (they have different
      names and properties in different languages and packages)
    * Create and solve a task, "How to select one or more columns from a table of data"
    * Create and solve a task, "How to select a subset of the rows from a table of data"
    * Create and solve a task, "How to add a new column to a table of data" (which is typically a
      column computed from other columns, or a constant or empty column to be edited later)
