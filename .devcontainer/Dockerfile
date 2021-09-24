# See here for image contents: https://hub.docker.com/r/jupyter/datascience-notebook/
FROM jupyter/datascience-notebook

# We would also like the following Python packages that don't come built in to
# the Jupyter datascience-notebook image:
USER jovyan
RUN pip3 --disable-pip-version-check --no-cache-dir \
    install rdatasets pingouin scikit_posthocs tabulate jupytext \
 && rm -rf /tmp/pip-tmp
# And these R packages that don't come built into the Jupyter datascience-notebook image:
RUN R -e 'install.packages("agricolae",repos="http://cran.us.r-project.org")'
RUN R -e 'install.packages("mosaic",repos="http://cran.us.r-project.org")'
RUN R -e 'install.packages("gplots",repos="http://cran.us.r-project.org")'
RUN R -e 'install.packages("nortest",repos="http://cran.us.r-project.org")'

# [Optional] Uncomment this section to install additional OS packages.
USER root
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
 && apt-get -y install --no-install-recommends ruby-full build-essential zlib1g-dev zip
USER jovyan
RUN mkdir ~/gems
ENV GEM_HOME=/home/jovyan/gems PATH="/home/jovyan/gems/bin:${PATH}"
RUN gem install jekyll bundler
