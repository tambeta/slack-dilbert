FROM python:3.8-alpine

ARG webhook_url

ARG INSTALL_DIR=/opt/dilbert
ARG CONFIG_DIR=/root/.config
ARG CACHE_DIR=/root/.cache
ARG CONFIG_FN=${CONFIG_DIR}/dilbertrc
ARG TS_FN=${CACHE_DIR}/dilbertts

WORKDIR ${INSTALL_DIR}

RUN /bin/mkdir -p ${INSTALL_DIR} ${CACHE_DIR} ${CONFIG_DIR}

RUN test -z "${webhook_url}" && echo 'The `webhook_url` build arg is mandatory' \
    && exit 1  || exit 0
RUN echo -e "[slack]\nwebhook_url=${webhook_url}" > $CONFIG_FN
RUN date +%Y-%m-%d > $TS_FN

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY dilbert.py .

