# ViReport minimal Docker image using Alpine base with Python
FROM python:3.7-alpine
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>

# install general dependencies
RUN apk update && apk add wget
