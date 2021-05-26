
# Specification of the `database/topics` folder

 * This folder will contain a set of Markdown files, one for each topic in the
   database for this website.
 * The name of each file in the filesystem will be a title succinctly
   describing the topic, such as `Bentley University GB213.md` or
   `Continuous Probability`.
    * We suggest the `.md` extension for Markdown files, rather than the
      alternative `.markdown`.
 * The files may link to images stored in the `database/topics/images`
   subfolder.  The Markdown code for this is the usual:
   `![Hover text here](images/image-file-name.png)`
 * The files may contain metadata in a YAML header.  Here is an example YAML
   header that could precede the actual Markdown content in a topic file:

```yaml
---
author:
 - Nathan Carter (ncarter@bentley.edu)
---
```
