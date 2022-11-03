
# How to Data

## Visit the website

This is a how-to website for students of data science.  It will contain
answers to a wide variety of how-to questions about data-related
software and programming languages.

[View the site online here.](https://how-to-data.org)

## Licenses

The website content is licensed under the
[CC-by-4.0](https://choosealicense.com/licenses/cc-by-4.0/) license.
This includes the contents of the `database/`, `jekyll-input/`, and `docs/`
folders within this repository.  Anyone submitting website content via a pull
request to this repository implicitly agrees that the work they are submitting
can be licensed by this project in that way, and that they have the right to
permit us to do so (e.g., by virtue of having written the content themselves).

The code that builds the website is licensed under the
[MIT license](https://choosealicense.com/licenses/mit/).
This includes all the rest of the repository outside the three folders
mentioned above.

## Building the website

The more common way for volunteers to contribute to this site is by
submitting new content, then letting the maintainers incorporate it into the
site.  See [the Contributing page of the
site](https://how-to-data.org/contributing/) for details.

However, if you have some need to build a local copy of the website, it is easy
to do so as follows.

1. Ensure that you have already installed
   [VSCode](https://code.visualstudio.com/),
   [Docker](https://www.docker.com/) desktop, and VSCode's
   [Remote - Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
1. Clone this repository to your local machine and open the folder in VSCode.
1. It will ask if you want to open the folder in the development container
   defined in the repository.  Say yes.
   
   (This will be very slow but only once.  The container image gets cached.)
1. To build the site, press `Ctrl+Alt+Shift+B` (on Mac `Cmd+Option+Shift+B`),
   VSCode's shortcut for "Run Build Task" and choose the option
   "Rebuild website and serve locally for testing."
   
   (Also very slow just once.  Later builds leverage a cache.)
1. When complete, visit the test site at `http://localhost:4000/`.
   To stop the local server, press `Ctrl+C`.

If you want to add content to the site, you may not want to rebuild the site
every time you make changes, despite the speed improvements of caching.  See
the `preview.py` script in this folder for a shortcut.
