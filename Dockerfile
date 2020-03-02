# ViReport minimal Docker image using Alpine base with Python
FROM alpine:latest
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>

# create temporary setup folder for everything
RUN mkdir VIREPORT_SETUP && \
    cd VIREPORT_SETUP

# install general programs
RUN apk update -q && \
    apk upgrade -q && \
    apk add -q --no-cache \
    autoconf \
    automake \
    bash \
    cmake \
    cython \
    file \
    g++ \
    gcc \
    libc-dev \
    libxml2-dev \
    linux-headers \
    make \
    py3-numpy \
    py3-numpy-dev \
    py3-scipy \
    python3 \
    python3-dev \
    R \
    R-dev \
    texlive \
    wget

# make bash the default shell and Python 3 the default Python
RUN sed -i 's/\/bin\/ash/\/bin\/bash/g' /etc/passwd
RUN ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip

# install Python 3 modules
RUN pip3 install -q biopython && \
    pip3 install -q bitsets && \
    pip3 install -q dendropy && \
    pip3 install -q niemads && \
    pip3 install -q seaborn && \
    pip3 install -q treeswift

# set up R
RUN echo "R_LIBS_SITE=\${R_LIBS_SITE-'/usr/local/lib/R/site-library:/usr/lib/R/library'}" >> /usr/lib/R/etc/Renviron && \
    echo 'options(repos = c(CRAN = "https://cloud.r-project.org/"))' >> /usr/lib/R/etc/Rprofile.site && \
    mkdir -p /usr/share/doc/R/html && \
    sed -i 's/CFLAGS =/CFLAGS = -D__USE_MISC/g' /etc/R/Makeconf && \
    R -e "install.packages(c('Rcpp'), INSTALL_opts = c('--no-html','--no-help','--no-html'), quiet=TRUE)" && \
    wget -q "https://github.com/r-lib/fs/archive/master.zip" && \
    unzip -q master.zip && \
    R CMD INSTALL fs-master > /dev/null && \
    rm -rf fs-master master.zip && \
    R -e "install.packages(c('devtools'), INSTALL_opts = c('--no-html','--no-help','--no-html'), quiet=TRUE)"

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

# install PhyML (3.3.20190909)
RUN wget -q "https://github.com/stephaneguindon/phyml/archive/master.zip" && \
    unzip -q master.zip && \
    cd phyml-master && \
    ./autogen.sh && \
    ./configure --enable-phyml && \
    make && \
    make install && \
    cd .. && \
    rm -rf phyml-master master.zip

# install RAxML-NG (0.9.0)
RUN wget -q "https://github.com/amkozlov/raxml-ng/releases/download/0.9.0/raxml-ng_v0.9.0_linux_x86_64.zip" && \
    unzip raxml-ng*.zip && \
    mv raxml-ng /usr/local/bin && \
    rm -rf raxml-ng*

# install treedater
RUN R -e "install.packages(c('devtools','ape','lpSolve','limSolve','getopt'))" && \
    R -e "library(devtools); install_github('emvolz/treedater', INSTALL_opts = c('--no-html','--no-help','--no-html'), quiet=TRUE)" && \
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
    ln -s /usr/local/bin/ViReport/ViReport.py /usr/local/bin/ViReport.py && \
    rm -rf master.zip

# clean up
RUN cd .. && \
    rm -rf VIREPORT_SETUP && \
    rm -f *.*

# run ViReport
ENTRYPOINT ["/bin/bash", "-c", "ViReport.py"]
