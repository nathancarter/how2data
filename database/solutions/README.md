
# Specification of the `database/solutions` folder

 * This folder will contain a set of Markdown files, one for each solution in
   the database for this website.
 * The path and filename of each file in the filesystem will clarify some key
   metadata, as follows.
    * Under the `database/solutions` folder will be a subfolder for each task
      in the `database/tasks` folder, so that for instance,
      `database/tasks/How to make a scatterplot.md` will correspond to
      `database/solutions/How to make a scatterplot/`.
    * Under each such task-named subfolder will be yet more folders, one for
      each software package for which we have solutions.  So for example, we
      might have a folder such as
      `database/solutions/How to make a scatterplot/Excel/`.
    * Inside each such software package-named subfolder will be various files
      containing solutions.  If there is just one such file, it can be named
      `solution.md`, but if there are several, they should have names that
      distinguish them, such as `using-VBA.md` and `without-VBA.md`.
    * We strongly suggest writing such solutions in Markdown rather than code,
      so that solutions can follow the convention of having excellent
      explanatory text surrounding the code.
 * Solution files may link to images stored in the same folder as the solution
   and they will be transferred to the website as part of the build process.
   The Markdown code for including images is the usual:
   `![Hover text here](image-file-name.png)`
 * Solution files may contain metadata in a YAML header.  Here is an example
   YAML header that could precede the actual Markdown content in a solutions file:

```yaml
---
author: Juan Grate Student (jgs@example.com)
tags:
 - simulation
 - random variables
---
```

(More to come.)
