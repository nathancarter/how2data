
# What are assignments?

It is often the case that a task in the database has a solution in software X
but not software Y.  We'd like to make it as easy as possible for someone who
knows software Y to write up a solution.

So we'd like to provide them with a document template in the format of
software Y that contains all the text from the solution in software X, plus
the code from software X, but commented out (since of course it will almost
never work in software Y), including comments stating what the output ought to
be (having computed them from software X), so that the author can compare
whatever they do in software Y with the known-to-be-correct answer.  Such a
file is called an *assignment.*

It is very easy to convert an assignment into a solution, as follows:

 1. Fill the code blocks (which start out full of comments only) with code to
    try to solve the problem.
 2. Compare the output to what's known to be correct (stored in the comments).
 3. Repeat until the correct output is given.
 4. Delete the old comments so that the new code is concise and readable.
 5. See if any of the text between code chunks needs to be updated to match
    software Y, in places where perhaps it spoke only of software X.

That completed assignment may be ready to drop into the `database/` folder
as is, or it may need a small amount of polishing work by this site's
maintainer.  Either way, it streamlines the process as much as possible.

# What is this folder for?

There is a script in this folder that can read the database, notice where
there are opportunities for assignments, and create such assignment files.

The resulting assignment files are, by default, also stored in this folder
(though they will not typically be committed to version control).
