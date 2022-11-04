# See here for image contents: https://hub.docker.com/r/jupyter/datascience-notebook/
FROM jupyter/datascience-notebook

# Install additional OS packages (some of which are needed for R/Python packages below):
USER root
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
 && apt-get -y install --no-install-recommends \
    ruby-full build-essential zlib1g-dev zip texlive-fonts-recommended lmodern

# Install the following Python packages that aren't built in to the above Dockerfile:
USER jovyan
RUN pip3 --disable-pip-version-check --no-cache-dir \
    install rdatasets pingouin scikit_posthocs tabulate jupytext \
 && rm -rf /tmp/pip-tmp

# Install the following R packages that aren't built in to the above Dockerfile:
RUN R -e 'install.packages("agricolae",repos="http://cran.us.r-project.org")'
RUN R -e 'install.packages("lattice",repos="http://cran.us.r-project.org")'
RUN R -e 'install.packages("gplots",repos="http://cran.us.r-project.org")'
RUN R -e 'install.packages("nortest",repos="http://cran.us.r-project.org")'
RUN R -e 'install.packages("DescTools",repos="http://cran.us.r-project.org")'
RUN R -e 'install.packages("emmeans",repos="http://cran.us.r-project.org")'
RUN R -e 'install.packages("rstatix",repos="http://cran.us.r-project.org")'
RUN R -e 'install.packages("ggpubr",repos="http://cran.us.r-project.org")'
RUN R -e 'install.packages("perm",repos="http://cran.us.r-project.org")'
RUN R -e 'install.packages("pwr",repos="http://cran.us.r-project.org")'
RUN R -e 'install.packages("gmodels",repos="http://cran.us.r-project.org")'

# And installing mosaic in this context requires special care:
RUN conda install -c conda-forge r-terra
RUN R -e 'install.packages("mosaic",repos="http://cran.us.r-project.org")'

# Install Jekyll for use in building the how2data website:
USER jovyan
RUN mkdir ~/gems
ENV GEM_HOME=/home/jovyan/gems PATH="/home/jovyan/gems/bin:${PATH}"
RUN gem install jekyll bundler
