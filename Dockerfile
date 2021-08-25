FROM nikolaik/python-nodejs:python3.6-nodejs15

ENV POETRY_VIRTUALENVS_CREATE false \
    PIP_NO_CACHE_DIR off \
    PIP_DISABLE_PIP_VERSION_CHECK on \
    PYTHONUNBUFFERED 1 \
    NODE_ENV production

ADD packages.txt /packages.txt
RUN set -ex; \
  curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -; \
  apt-get update; \
  cat /packages.txt | grep -v \# | xargs apt-get install -y; \
  # cleaning up unused files \
  apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
  rm -rf /var/lib/apt/lists/*


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
