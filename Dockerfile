# ViReport Docker image using Ubuntu 20.04 base
FROM ubuntu:20.04
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>

# create temporary setup folder for everything
RUN mkdir VIREPORT_SETUP && \
    cd VIREPORT_SETUP

# install general programs
RUN apt-get update -q && apt-get upgrade -y -q && apt-get install -y -q \
    curl \
    gfortran \
    less \
    libbz2-dev \
    libcurl4-openssl-dev \
    liblzma-dev \
    libpcre3-dev \
    libreadline-dev \
    python3 \
    python3-pip \
    texinfo \
    texlive-latex-base \
    wget \
    xorg-dev
RUN ln -s $(which python3) /usr/local/bin/python

# set up Python 3 packages
RUN pip3 install -q biopython && \
    pip3 install -q bitsets && \
    pip3 install -q dendropy && \
    pip3 install -q niemads && \
    pip3 install -q seaborn && \
    pip3 install -q treeswift

# set up R (3.6.3)
RUN wget -qO- "https://cran.r-project.org/src/base/R-3/R-3.6.3.tar.gz" | tar -zx && \
    cd R-* && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf R-*
RUN wget -qO- "https://stat.ethz.ch/R/daily/R-devel.tar.gz" | tar -zx && \
    cd R-devel && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf R-devel
RUN echo 'options(repos = c(CRAN = "https://cloud.r-project.org/"))' >> /usr/local/lib/R/etc/Rprofile.site && \
    R -e "install.packages(c('fs','devtools','BiocManager'), quiet=TRUE)"

# clean up
RUN cd .. && \
    rm -rf VIREPORT_SETUP && \
    rm -f *.*

# run ViReport
ENTRYPOINT ["/bin/bash", "-c", "ViReport.py"]
