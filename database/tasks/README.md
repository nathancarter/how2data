
# Specification of the `database/tasks` folder

 * This folder will contain a set of Markdown files, one for each task in the
   database for this website.
 * The name of each file in the filesystem will be a title succinctly
   describing the task, such as `How to make a scatterplot.md`.
    * We suggest the `.md` extension for Markdown files, rather than the
      alternative `.markdown`.
    * We suggest that each task title begin with the phrase "How to," for both
      consistency among the tasks and to fit with the title of the website.
 * The files may link to images stored in the `database/tasks/images`
   subfolder.  The Markdown code for this is the usual:
   `![Hover text here](images/image-file-name.png)`
 * The files may contain metadata in a YAML header.  Here is an example YAML
   header that could precede the actual Markdown content in a task file:

```yaml
---
tags:
 - statistics
 - visualization
---
```
