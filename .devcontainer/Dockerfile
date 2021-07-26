# See here for image contents: https://hub.docker.com/r/jupyter/datascience-notebook/
FROM jupyter/datascience-notebook

# We would also like the following Python packages that don't come built in to
# the Jupyter datascience-notebook image:
USER jovyan
RUN pip3 --disable-pip-version-check --no-cache-dir \
    install rdatasets pingouin \
 && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
USER root
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
 && apt-get -y install --no-install-recommends ruby-full build-essential zlib1g-dev zip
USER jovyan
RUN mkdir ~/gems
ENV GEM_HOME=/home/jovyan/gems PATH="/home/jovyan/gems/bin:${PATH}"
RUN gem install jekyll bundler
