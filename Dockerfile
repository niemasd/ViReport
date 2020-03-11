# ViReport Docker image using Ubuntu 20.04 base
FROM ubuntu:20.04
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>

# create temporary setup folder for everything
RUN mkdir VIREPORT_SETUP && \
    cd VIREPORT_SETUP

# install general programs
RUN apt-get update -q && apt-get upgrade -y -q && apt-get install -y -q \
    autoconf \
    cmake \
    curl \
    gfortran \
    less \
    libbz2-dev \
    libcurl4-openssl-dev \
    liblzma-dev \
    libpcre3-dev \
    libreadline-dev \
    libssl-dev \
    libxml2-dev \
    python3 \
    python3-pip \
    texinfo \
    texlive-latex-base \
    unzip \
    wget \
    xorg-dev \
    zip
RUN ln -s $(which python3) /usr/local/bin/python

# set up Python 3 packages
RUN pip3 install -q biopython && \
    pip3 install -q bitsets && \
    pip3 install -q cython && \
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

# install Clustal Omega (1.2.4)
RUN wget -qO- "http://prdownloads.sourceforge.net/argtable/argtable2-13.tar.gz" | tar -zx && \
    cd argtable* && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf argtable*
RUN wget -qO- "http://www.clustal.org/omega/clustal-omega-1.2.4.tar.gz" | tar -zx && \
    cd clustal-omega* && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf clustal-omega*

# install FastRoot
RUN wget -q "https://github.com/uym2/MinVar-Rooting/archive/master.zip" && \
    unzip -q master.zip && \
    mv MinVar-Rooting-master /usr/local/bin/MinVar-Rooting && \
    ln -s /usr/local/bin/MinVar-Rooting/FastRoot.py /usr/local/bin/FastRoot.py && \
    rm -rf MinVar-Rooting-master master.zip

# install FastTree
RUN wget -q "http://www.microbesonline.org/fasttree/FastTree.c" && \
    gcc -DUSE_DOUBLE -DOPENMP -fopenmp -O3 -finline-functions -funroll-loops -Wall -o FastTree FastTree.c -lm && \
    mv FastTree /usr/local/bin && \
    rm FastTree.c

# install ggtree
RUN R -e "BiocManager::install('ggtree', quiet=TRUE)"

# install HIV-TRACE
RUN wget -q "https://github.com/veg/tn93/archive/master.zip" && \
    unzip master.zip && \
    cd tn93-master && \
    cmake . && \
    make install && \
    cd .. && \
    rm -rf tn93-master master.zip
#RUN pip3 install -q hivtrace

# clean up
RUN cd .. && \
    rm -rf VIREPORT_SETUP && \
    rm -f *.*

# install IQ-TREE (1.6.12)
RUN wget -qO- "https://github.com/Cibiv/IQ-TREE/releases/download/v1.6.12/iqtree-1.6.12-Linux.tar.gz" | tar -zx && \
    mv iqtree*/bin/iqtree /usr/local/bin && \
    rm -rf iqtree*

# install LogDate
RUN wget -q "https://github.com/uym2/LogDate/archive/master.zip" && \
    unzip -q master.zip && \
    mv LogDate-master/Software /usr/local/bin/LogDate && \
    ln -s /usr/local/bin/LogDate/launch_LogDate.py /usr/local/bin/launch_LogDate.py && \
    rm -rf LogDate-master master.zip

# install LSD2
RUN wget -q "https://github.com/tothuhien/lsd2/archive/master.zip" && \
    unzip -q master.zip && \
    cd lsd2-master/src && \
    make && \
    mv lsd2 /usr/local/bin && \
    cd ../.. && \
    rm -rf lsd2-master master.zip

# install MAFFT (7.453)
RUN wget -qO- "https://mafft.cbrc.jp/alignment/software/mafft-7.453-without-extensions-src.tgz" | tar -zx && \
    cd mafft*/core && \
    make clean && \
    make && \
    make install && \
    cd ../.. && \
    rm -rf mafft*

# install MUSCLE (3.8.31)
RUN wget -qO- "https://www.drive5.com/muscle/downloads3.8.31/muscle3.8.31_i86linux64.tar.gz" | tar -zx && \
    mv muscle* /usr/local/bin/muscle

# install PhyML
RUN wget -q "https://github.com/stephaneguindon/phyml/archive/master.zip" && \
    unzip -q master.zip && \
    cd phyml-master && \
    ./autogen.sh && \
    ./configure --enable-phyml CFLAGS='-mavx' && \
    make CFLAGS='-mavx' && \
    make install && \
    cd .. && \
    rm -rf phyml-master master.zip

# install RAxML-NG (0.9.0)
RUN wget -q "https://github.com/amkozlov/raxml-ng/releases/download/0.9.0/raxml-ng_v0.9.0_linux_x86_64.zip" && \
    unzip raxml-ng*.zip && \
    mv raxml-ng /usr/local/bin && \
    rm -rf raxml-ng*

# install treedater
RUN R -e "install.packages(c('devtools','ape','lpSolve','limSolve','getopt'), quiet=TRUE)" && \
    R -e "library(devtools); install_github('emvolz/treedater', quiet=TRUE)" && \
    wget -qO- "https://raw.githubusercontent.com/emvolz/treedater/master/inst/tdcl" > /usr/local/bin/tdcl && \
    chmod a+x /usr/local/bin/tdcl

# run ViReport
ENTRYPOINT ["/bin/bash", "-c", "ViReport.py"]
