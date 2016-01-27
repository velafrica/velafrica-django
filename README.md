# Setup

1. Install Postgres
on ubuntu: https://help.ubuntu.com/community/PostgreSQL
1.1. download and install
sudo apt-get install postgresql postgresql-contrib
ssudo apt-get install postgresql-client
1.1.1. (optional) install pgadmin
sudo apt-get install pgadmin3
1.2. create user
sudo -u postgres createuser --superuser $USER
1.3. create database
sudo -u postgres createdb $USER 


# Getting started with Django on Heroku
https://devcenter.heroku.com/articles/django-app-configuration#creating-a-new-django-project