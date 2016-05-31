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

# Database
https://devcenter.heroku.com/articles/heroku-postgresql#local-setup
DATABASE_URL: postgres://<username>:<password>@<host>/<dbname>

# Most helpful heroku toolkit cmds
`heroku login` login to heroku

`heroku config --app velafrica-admin` show all env variables

`heroku config:set ON_HEROKU=1 --app velafrica-admin` set ENV variable (necessary for choosing the right database)

`heroku ps:psql --app velafrica-admin

# Postgres command to reset currentt id
    select id from auth_group order by id DESC LIMIT 1;
     id 
    ----
     11
    alter sequence auth_group_id_seq restart with 12;

 created by Platzh1rsch (www.platzh1rsch.ch)