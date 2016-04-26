# Dev environment
#
# Makes a virtualenv at /venv which might need updating but should
# have a good base of dependencies.
#
# 420fd03947ad


FROM ubuntu:trusty

ADD requirements.txt /requirements.txt

RUN apt-get update -y && \
    apt-get install -y software-properties-common && \
    apt-add-repository -y ppa:ubuntugis/ubuntugis-unstable && \
    apt-get update -y && \
    apt-get install -y  libgdal-dev=1.11* \
                        python-pip \
                        python-virtualenv \
                        git \
                        python-gdal \
                        libgdal1-dev \
                        libncurses5-dev \
                        python-psycopg2 \
                        python-dev && \
    virtualenv venv && \
    ln -snf /bin/bash /bin/sh

RUN source venv/bin/activate && \
    pip install -r /requirements.txt

CMD ["/bin/bash"]
