FROM ubuntu:latest
RUN apt-get update -y

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip\
  && apt-get install -y libmysqlclient-dev

ENV DEBIAN_FRONTEND=noninteractive 
RUN apt-get install -y openssh-server

# TODO: Check if docker compose can do this
ARG DB_HOST
ENV DB_HOST ${DB_HOST}

ARG MYSQL_DB_BIND
ENV MYSQL_DB_BIND ${MYSQL_DB_BIND}

ARG MEMSQL_DB_BIND
ENV MEMSQL_DB_BIND ${MEMSQL_DB_BIND}

ARG AUTH0_CLIENT_ID
ENV AUTH0_CLIENT_ID ${AUTH0_CLIENT_ID}

ARG AUTH0_CLIENT_SECRET
ENV AUTH0_CLIENT_SECRET ${AUTH0_CLIENT_SECRET}

COPY ./app /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# Migrations
# RUN python3 manage.py db upgrade
CMD ["gunicorn","-b","0.0.0.0:5000","wsgi"]

