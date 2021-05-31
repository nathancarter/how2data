
# Specification of the `database/tasks` folder

 * This folder will contain a set of Markdown files, one for each task in the
   database for this website.
 * The name of each folder in the filesystem will be a title succinctly
   describing the task, such as `How to make a scatterplot`.  Each task title
   should begin with the phrase "How to," both for consistency among the tasks
   and to fit with the title of the website.
 * Each such folder will contain a description of the task stored in a file
   named `description.md`, stored immediately inside the task folder.
 * That description file may link to images stored in the same task folder.
   The Markdown code for this is the usual:
   `![Hover text here](image-file-name.png)`
 * The description files may contain metadata in a YAML header.  Here is an
   example YAML header that could precede the actual Markdown content in a
   task description file:

```yaml
---
tags:
 - statistics
 - visualization
---
```

 * Under each task folder will be yet more folders, one for each software
   package for which we have solutions.  So for example, we might have a
   folder such as `database/tasks/How to make a scatterplot/Excel/`.
 * Inside each such software package-named subfolder will be various files
   containing solutions.  If there is just one such file, it can be named
   `solution.md`, but if there are several, they should have names that
   distinguish them, such as `using VBA.md` and `without VBA.md`.
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
