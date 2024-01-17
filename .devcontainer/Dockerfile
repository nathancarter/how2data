# See here for image contents: https://hub.docker.com/r/jupyter/datascience-notebook/
FROM jupyter/datascience-notebook:2023-05-30

# Package installation steps for the OS need to be done as root
USER root

# Install additional OS packages (some of which are needed for R/Python packages below)
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
 && apt-get -y install --no-install-recommends \
    ruby-full build-essential zlib1g-dev zip texlive-fonts-recommended lmodern cmake

# Do all other steps using the account the VS Code user will use
USER jovyan

# Note: Steps below are sequenced primarily to ensure that A precedes B iff A is
# needed for B to work, but secondarily sequenced to put frequently edited things
# later in the list, to minimize container rebuild times.

# Install Jekyll, which is our static site generator
RUN mkdir ~/gems
ENV GEM_HOME=/home/jovyan/gems PATH="/home/jovyan/gems/bin:${PATH}"
RUN gem install jekyll bundler

# Install the following Python packages that aren't part of the Jupyter
# datascience-notebook image
RUN pip3 --disable-pip-version-check --no-cache-dir install \
    rdatasets pingouin scikit_posthocs tabulate jupytext streamlit \
    openai python-dotenv \
 && rm -rf /tmp/pip-tmp

# Install the following Julia packages that aren't part of the Jupyter
# datascience-notebook image
RUN julia -e 'using Pkg; Pkg.add("DataFrames")'
RUN julia -e 'using Pkg; Pkg.add("Plots")'
RUN julia -e 'using Pkg; Pkg.add("Statistics")'
RUN julia -e 'using Pkg; Pkg.add("RDatasets")'
RUN julia -e 'using Pkg; Pkg.add("Distributions")'
RUN julia -e 'using Pkg; Pkg.add("HypothesisTests")'
RUN julia -e 'using Pkg; Pkg.add("GLM")'

# Install the following R packages that aren't part of the Jupyter
# datascience-notebook image
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
RUN R -e 'install.packages("anytime",repos="http://cran.us.r-project.org")'

# And installing mosaic in this context requires special care:
RUN conda install -c conda-forge r-terra
RUN R -e 'install.packages("mosaic",repos="http://cran.us.r-project.org")'
