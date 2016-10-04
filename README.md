# Info

`ch.velafrica.admin` can be looked at on [http://tracking.velafrica.ch](http://tracking.velafrica.ch) at the moment.

This project is kind of an ERP (Enterprise resource planning) system for the people at Velafrica ( [http://velafrica.ch](http://velafrica.ch) ).
It is consisting of different modules, all serving the purpose to manage specific processes and teams inside Velafrica.

The modules are:

- collection
- commission
- core
- counter
- download
- organisation
- sbbtracking
- stock
- transport
- velafrica_sud

Furthermore there are two special modules:

- api (specification and handling for the rest api)
- frontend (all the html stuff for the frontend)

## Technology
`ch.velafrica.admin` is a Django application, using various 3rd party packages for additional features. Django is a very well known python framework to develop web applications. On the frontend, bootstrap is used to avoid the pain of building yet another responsive website from scratch.

## Learning resources
If you do not know much about Django or Bootstrap yet, we can recommend the following sites to extend your knowledge:

- [https://www.djangoproject.com/](https://www.djangoproject.com/)
- [http://getbootstrap.com/](http://getbootstrap.com/)

## Recommended tools
We recommend using [PyCharm by IntelliJ](https://www.jetbrains.com/pycharm/) (full IDE) or Sublime Text (enhanced Text editor) to work on the code.

# Setup

## Required software

- python (>2.7, <3.0)
- python-pip
- virtualenv
- sqlite3

For help on how to get pip and virtualenv running on Windows, take a look at [this](http://pymote.readthedocs.io/en/latest/install/windows_virtualenv.html).

## Getting started
The 6 steps to get you started.

### 1. Setup virtualenv
Virtualenv is here to provide an isolated environment for your app, with its own python runtime and python packages.
Navigate into the project directory and type the following command:

    virtualenv env

This creates a virtual environment in a newly created `env` folder, inside of your project directory.
### 2. Activate virtualenv

#### Windows

    ./env/Scripts/activate

#### Linux / Mac

    source env/bin/activate

### 3. Install packages

    pip install -r requirements.txt

### 4. Create database (apply migrations)
   
    python manage.py migrate

### 5. Start development server

    python manage.py runserver

### 6. Enjoy

Take a look at the result on [http://localhost:8000/](http://localhost:8000/) :-)

TODO: describe required env variables

-----------------------------------------------------------------------------

# [deprecated]
The following sections are outdated and need an update

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

`heroku pg:psql --app velafrica-admin

# Postgres command to reset currentt id
    select id from auth_group order by id DESC LIMIT 1;
     id 
    ----
     11
    alter sequence auth_group_id_seq restart with 12;

 created by Platzh1rsch (www.platzh1rsch.ch)