from python:3.6
run apt-get update && apt-get install -y \
   gettext \
   git \
   gunicorn \
   postgresql-common \
   postgresql-client \
   libcairo2 \
   libffi6 \
   libgdk-pixbuf2.0-0

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get -qq update; apt-get -y install nodejs

run pip3 install pipenv

RUN useradd test
RUN chsh test -s /bin/bash
RUN mkdir /home/test -p ; chown test -R /home/test ; chgrp test /home/test
RUN ls -la /home/test
