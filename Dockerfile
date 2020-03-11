# ViReport Docker image using Ubuntu 20.04 base
FROM ubuntu:20.04
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>

# create temporary setup folder for everything
RUN mkdir VIREPORT_SETUP && \
    cd VIREPORT_SETUP

# set up environment (update Ubuntu and install Miniconda)
RUN apt-get update -q && apt-get upgrade -y -q && apt-get install -y -q wget
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /usr/local/bin/miniconda3 && \
    rm Miniconda3-latest-Linux-x86_64.sh

# Make RUN commands use the new environment:
SHELL ["/usr/local/bin/miniconda3/bin/conda", "run", "-n", "myenv", "/bin/bash", "-c"]
RUN conda init
