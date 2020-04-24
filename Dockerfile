FROM ubuntu:latest
RUN apt-get update -y

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN apt-get install -y openssh-server

# TODO: Check if docker compose can do this
ARG DB_HOST
ENV DB_HOST ${DB_HOST}

COPY ./app /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# Migrations
# RUN python3 manage.py db upgrade

ENTRYPOINT ["python3"]
CMD ["run.py"]