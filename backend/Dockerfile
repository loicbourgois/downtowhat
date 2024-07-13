FROM python:3.10
RUN wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy \
  && chmod +x ./cloud_sql_proxy \
  && mkdir -p /root/github.com/loicbourgois/bin \
  && mv cloud_sql_proxy /root/github.com/loicbourgois/bin/cloud_sql_proxy
RUN apt-get clean \
    && apt-get update  \
    && apt-get install -y screen
ENV PATH="${PATH}:/root/github.com/loicbourgois/bin/"
COPY backend/requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip python -m pip install -r requirements.txt
COPY backend/inner.sh /root/github.com/loicbourgois/backend/backend/inner.sh
