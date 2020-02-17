# ViReport minimal Docker image using Alpine base with Python
FROM python:3.7-alpine
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>

# install general programs
RUN apk update && apk add wget

# install Python 3 modules
RUN pip install dendropy && \
    pip install niemads && \
    pip install treeswift

# install FastRoot
RUN wget https://github.com/uym2/MinVar-Rooting/archive/master.zip && unzip master.zip && \
    mv MinVar-Rooting-master /usr/local/bin/MinVar-Rooting && \
    ln -s /usr/local/bin/MinVar-Rooting/FastRoot.py /usr/local/bin/FastRoot.py && \
    rm -rf MinVar-Rooting-master master.zip
