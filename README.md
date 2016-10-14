# tracking.velafrica.ch

This project is an ERP (Enterprise resource planning) system for the people at Velafrica ( [http://velafrica.ch](http://velafrica.ch) ).
It consists of different modules, all serving the purpose to manage specific processes and teams inside Velafrica.

# Table of contents

  * [Detailed description](#detailed-description)
  * [Technology](#technology)
  * [Learning resources](#learning-resources)
  * [Recommended tools](#recommended-tools)
  * [Setup](#setup)
    * [Required software](#required-software)
    * [Getting started](#getting-started)

## Detailed description

`ch.velafrica.admin` can be looked at on [http://tracking.velafrica.ch](http://tracking.velafrica.ch) at the moment.

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
    - macOS: `brew install python`
    - Windows: download installer from https://www.python.org/downloads/release/python-2712/
- python-pip
- virtualenv
    - Windows: http://pymote.readthedocs.io/en/latest/install/windows_virtualenv.html
- postgresql (9.4)
- node (5.5): https://nodejs.org/download/release/v5.5.0/
- heroku toolbelt: https://devcenter.heroku.com/articles/heroku-command-line#download-and-install

## Getting started

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

TODO: [make ready for prod deployment](https://docs.djangoproject.com/en/1.10/ref/django-admin/#cmdoption-check--deploy)
