FROM python:3.9-alpine

ARG INSTALL_DIR=/opt/dilbert

WORKDIR ${INSTALL_DIR}
RUN /bin/mkdir -p ${INSTALL_DIR}

COPY dilbert.py requirements.txt ./
COPY lib lib/
RUN pip install --no-cache-dir -r requirements.txt

