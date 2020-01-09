FROM python:3.8-alpine

ARG INSTALL_DIR=/opt/dilbert

WORKDIR ${INSTALL_DIR}
RUN /bin/mkdir -p ${INSTALL_DIR}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY dilbert.py .

