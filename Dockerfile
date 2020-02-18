# ViReport minimal Docker image using Alpine base with Python
FROM python:3.7-alpine
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>

# install general programs
RUN apk update && apk add gcc libc-dev make wget

# install Python 3 modules
RUN pip install dendropy && \
    pip install niemads && \
    pip install treeswift

# install FastRoot
RUN wget -q https://github.com/uym2/MinVar-Rooting/archive/master.zip && \
    unzip master.zip && \
    mv MinVar-Rooting-master /usr/local/bin/MinVar-Rooting && \
    ln -s /usr/local/bin/MinVar-Rooting/FastRoot.py /usr/local/bin/FastRoot.py && \
    rm -rf MinVar-Rooting-master master.zip

# install MAFFT
RUN wget -qO- "https://mafft.cbrc.jp/alignment/software/mafft-7.453-without-extensions-src.tgz" | tar -zx && \
    cd mafft*/core && \
    make clean && \
    make && \
    make install && \
    cd ../.. && \
    rm -rf mafft*
