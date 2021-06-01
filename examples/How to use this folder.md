
# How to use this folder

This folder is geared towards anyone who wants to contribute new tasks and/or
solutions to the website [*How to Data*](https://nathancarter.github.io/how2data/site/).

## If you want to work in Python

(See later in this document for working in R or some other software.)

Inside the Python subfolder, you will find a folder entitled
"How to print a caterpillar."  Obviously, this is a silly task meant only for
use as an example.

 * If you're adding a new task to the *How to Data* database, do this:
    * Rename the folder from "How to print a caterpillar" to the name of your
      task.  It should still begin with "How to," such as "How to create a
      scatterplot."
    * Edit the notebook `description.ipynb` in that folder and edit it to
      describe your task, instead of the example caterpillar task.
 * If you're not providing a solution to your task, delete the file
   `Python.ipynb`.
 * If you are providing a solution with your task, open the Jupyter notebook
   `Python.ipynb` in that folder and edit it to show a solution to your task,
   instead of the caterpillar task.
    * The notebook is named `Python.ipynb` because it is a solution that uses
      Python.
    * If you are using Python plus some important packages, please rename the
      notebook to something like `Python, using pandas.ipynb` or
      `Python, using Matplotlib and SciPy.ipynb`.  Note the commas, which are
      important.

To submit your new task and/or solution, visit
[the folder on GitHub](https://github.com/nathancarter/how2data/tree/main/database/tasks-and-solutions)
where the *How to Data* tasks and solutions live.
You will upload your work there in one of two ways:

 * If you created a task (and optionally a solution with it), do this:
    * Click "Add file" and then "Upload files."
    * Drag the task folder you renamed (e.g., "How to create a scatterplot")
      into your browser to upload it.
    * Under the "Commit changes" heading, write a short phrase to explain what
      you're submitting, such as "Adding scatterplot task with Python
      solution."
    * Make sure you're creating a new branch and a pull request. (A "pull
      request" is a request for the *How to Data* maintainers to review and
      accept your submission.)
    * Click "Commit changes."
 * If you created a solution to a task that already exists in the site, do
   this instead:
    * In your browser, click to enter the subfolder for the task in question.
    * Click "Add file" and then "Upload files."
    * Drag *just your new solution file* (e.g. `Python.ipynb` or
      `Python, using pandas.ipynb`) in to upload it.  (Do not upload your
      whole task folder, just the solution file that's in that folder.)
    * Under the "Commit changes" heading, write a short phrase to explain what
      you're submitting, such as "Adding a Python solution to the scatterplot
      task."
    * Make sure you're creating a new branch and a pull request (which means
      you're asking the *How to Data* maintainers to accept your submission).
    * Click "Commit changes."

The team in charge of *How to Data* will (very gratefully!) review your work and contact you soon.  Thank you!

## If you want to work in R

(See later in this document for working in other software.)

Inside the R subfolder, you will find a folder entitled
"How to print a caterpillar."  Obviously, this is a silly task meant only for
use as an example.

 * If you're adding a new task to the *How to Data* database, do this:
    * Rename the folder from "How to print a caterpillar" to the name of your
      task.  It should still begin with "How to," such as "How to create a
      scatterplot."
    * Edit the RMarkdown notebook `description.Rmd` in that folder and edit it
      to describe your task, instead of the example caterpillar task.
 * If you're not providing a solution to your task, delete the file `R.Rmd`.
 * If you are providing a solution to your task, open the RMarkdown notebook
   `R.Rmd` in that folder and edit it to show a solution to your task, instead
   of the caterpillar task.
    * The notebook is named `R.Rmd` because it is a solution that uses R.
    * If you are using R plus some important packages, please rename the
      notebook to something like `R, using dplyr.Rmd` or
      `R, using ggplot2.Rmd`.  Note the commas, which are important.

To submit your new task and/or solution, visit
[the folder on GitHub](https://github.com/nathancarter/how2data/tree/main/database/tasks-and-solutions)
where the *How to Data* tasks and solutions live.
You will upload your work there in one of two ways:

 * If you created a task (and optionally a solution with it), do this:
    * Click "Add file" and then "Upload files."
    * Drag the task folder you renamed (e.g., "How to create a scatterplot")
      into your browser to upload it.
    * Under the "Commit changes" heading, write a short phrase to explain what
      you're submitting, such as "Adding scatterplot task with R solution."
    * Make sure you're creating a new branch and a pull request (which means
      you're asking the *How to Data* maintainers to accept your submission).
    * Click "Commit changes."
 * If you created a solution to a task that already exists in the site, do
   this instead:
    * In your browser, click to enter the subfolder for the task in question.
    * Click "Add file" and then "Upload files."
    * Drag *just your new solution file* (e.g. `R.Rmd` or
      `R, using ggplot2.Rmd`) in to upload it.  (Do not upload your
      whole task folder, just the solution file that's in that folder.)
    * Under the "Commit changes" heading, write a short phrase to explain what
      you're submitting, such as "Adding an R solution to the scatterplot
      task."
    * Make sure you're creating a new branch and a pull request. (A "pull
      request" is a request for the *How to Data* maintainers to review and
      accept your submission.)
    * Click "Commit changes."

The team in charge of *How to Data* will (very gratefully!) review your work and contact you soon.  Thank you!

## If you want to submit solutions in more than one language

Simply follow the instructions for each language separately, above.

## If you want to submit a solution in software besides Python or R

Follow the instructions for either Python or R, but rename your solution file
from `Python.ipynb` to `Excel.ipynb` or from `R.Rmd` to `Excel.Rmd`, or
whatever software you're documenting.  Examples:

 * `SPSS.ipynb`
 * `Excel, using VBA.Rmd`
 * etc.

Submit in the same way as documented for Python and/or R.

## Notes

It is acceptable to include images in the folder being submitted, and
reference those images from within the `.ipynb` or `.Rmd` solution files, as
figures.

It is also acceptable to write solution files in `.md` or `.markdown`
format, in addition to the `.ipynb` and `.Rmd` formats.
