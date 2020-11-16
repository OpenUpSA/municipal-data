FROM nikolaik/python-nodejs:python3.6-nodejs15

ENV POETRY_VIRTUALENVS_CREATE false
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PYTHONUNBUFFERED 1
ENV NODE_ENV production

ADD packages.txt /packages.txt
RUN set -ex; \
  apt-get update; \
  cat /packages.txt | grep -v \# | xargs apt-get install -y; \
  # cleaning up unused files \
  apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
  rm -rf /var/lib/apt/lists/*
RUN set -ex; \
  wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb; \
  dpkg --install wkhtmltox_0.12.6-1.buster_amd64.deb; \
  rm wkhtmltox_0.12.6-1.buster_amd64.deb


ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /app

ARG USER_ID=1001
ARG GROUP_ID=1001

RUN set -ex; \
  addgroup --gid $GROUP_ID --system django; \
  adduser --system --uid $USER_ID --gid $GROUP_ID django; \
  chown -R django:django /app
USER django

WORKDIR /app

RUN set -ex; \
  yarn; \
  yarn build

EXPOSE 5000
CMD /app/bin/start-web.sh
