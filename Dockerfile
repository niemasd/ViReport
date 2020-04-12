# ViReport Docker image using miniconda3 base
FROM continuumio/miniconda3:latest
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>
SHELL ["/bin/bash", "-c"]

# create temporary setup folder for everything
RUN mkdir /VIREPORT_SETUP
WORKDIR /VIREPORT_SETUP

# install required general programs
RUN apt-get update -q && apt-get upgrade -y -q && apt-get install -y -q autoconf cmake g++ gcc libtool make unzip wget yaggo && \
    ln -s /bin/tar /bin/gtar

# set up Python 3 packages
RUN pip install -q biopython && \
    pip install -q bitsets && \
    pip install -q cython && \
    pip install -q dendropy && \
    pip install -q niemads && \
    pip install -q pdf2image && \
    pip install -q phylo-treetime && \
    pip install -q python-docx && \
    pip install -q seaborn && \
    pip install -q treeswift

# set up R
RUN conda install -q -y r && \
    conda install -q -y -c conda-forge r-devtools && \
    echo 'options(repos = c(CRAN = "https://cloud.r-project.org/"))' >> /opt/conda/lib/R/etc/Rprofile.site

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

# install FSA (1.15.9)
RUN wget -q "https://github.com/mummer4/mummer/archive/master.zip" && \
    unzip master.zip && \
    cd mummer-master && \
    autoreconf -fi && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf mummer-master master.zip && \
    ldconfig
RUN wget -qO- "http://ftp.ebi.ac.uk/pub/software/vertebrategenomics/exonerate/exonerate-2.2.0-x86_64.tar.gz" | tar -zx && \
    mv exonerate*/bin/* /usr/local/bin && \
    mkdir -p /usr/local/share/man/man1 && \
    mv exonerate*/share/man/man1/* /usr/local/share/man/man1 && \
    rm -rf exonerate*
RUN wget -qO- "https://ayera.dl.sourceforge.net/project/fsa/fsa-1.15.9.tar.gz" | tar -zx && \
    cd fsa* && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf fsa*

# install Kalign (3.2.3)
RUN wget -qO- "https://github.com/TimoLassmann/kalign/archive/v3.2.3.tar.gz" | tar -zx && \
    cd kalign-* && \
    ./autogen.sh && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf kalign-*

# install HIV-TRACE
RUN wget -q "https://github.com/veg/tn93/archive/master.zip" && \
    unzip master.zip && \
    cd tn93-master && \
    cmake . && \
    make install && \
    cd .. && \
    rm -rf tn93-master master.zip
#RUN pip3 install -q hivtrace

# install IQ-TREE (1.6.12)
RUN wget -qO- "https://github.com/Cibiv/IQ-TREE/releases/download/v1.6.12/iqtree-1.6.12-Linux.tar.gz" | tar -zx && \
    mv iqtree*/bin/iqtree /usr/local/bin && \
    rm -rf iqtree*

# install LogDate
RUN wget -q "https://github.com/uym2/LogDate/archive/master.zip" && \
    unzip -q master.zip && \
    mv LogDate-master/Software /usr/local/bin/LogDate && \
    ln -s /usr/local/bin/LogDate/launch_LogDate.py /usr/local/bin/LogDate.py && \
    rm -rf LogDate-master master.zip /usr/local/bin/LogDate/dendropy/test

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

# install PRANK (170427)
RUN wget -qO- "http://wasabiapp.org/download/prank/prank.linux64.170427.tgz" | tar -zx && \
    mv prank/bin/* /usr/local/bin && \
    rm -rf prank

# install RAxML-NG (0.9.0)
RUN wget -q "https://github.com/amkozlov/raxml-ng/releases/download/0.9.0/raxml-ng_v0.9.0_linux_x86_64.zip" && \
    unzip raxml-ng*.zip && \
    mv raxml-ng /usr/local/bin && \
    rm -rf raxml-ng*

# install treedater
RUN R -e "install.packages(c('ape','lpSolve','limSolve','getopt'), quiet=TRUE)" && \
    R -e "library(devtools); install_github('emvolz/treedater', quiet=TRUE)" && \
    wget -qO- "https://raw.githubusercontent.com/emvolz/treedater/master/inst/tdcl" > /usr/local/bin/tdcl && \
    chmod a+x /usr/local/bin/tdcl

# install TreeN93
RUN wget -qO- "https://raw.githubusercontent.com/niemasd/TreeN93/master/TreeN93.py" > /usr/local/bin/TreeN93.py && \
    wget -qO- "https://raw.githubusercontent.com/niemasd/TreeN93/master/TreeN93_cluster.py" > /usr/local/bin/TreeN93_cluster.py && \
    chmod a+x /usr/local/bin/TreeN93*.py

# set up ViReport
RUN wget -q "https://github.com/niemasd/ViReport/archive/master.zip" && \
    unzip -q master.zip && \
    mv ViReport-master /usr/local/bin/ViReport && \
    chmod a+x /usr/local/bin/ViReport/ViReport.py && \
    alias ViReport.py='/usr/local/bin/ViReport/ViReport.py' && \
    rm -rf master.zip

# clean up
WORKDIR /
RUN rm -rf /VIREPORT_SETUP

# run ViReport
ENTRYPOINT ["/bin/bash", "-c", "ViReport.py"]
