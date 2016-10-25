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

```bash
virtualenv venv
```

This creates a virtual environment in a newly created `venv` folder, inside of your project directory.

### 2. Activate virtualenv

#### Windows

```bash
./venv/Scripts/activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### 3. Install packages

```bash
pip install -r requirements.txt
npm install
```

*There is a problem installing libxml on Windows machines, follow [this](http://stackoverflow.com/questions/30493031/installing-lxml-libxml2-libxslt-on-windows-8-1) to get it working.

### 4. Define the environment variables

```bash
cp .env_dist .env
```

And then fill in your database credentials (eg. username, password & database name) in `.env`

### 5. Create database (apply migrations)
   
```bash
heroku local:run python manage.py migrate
```

### 6. Start development server & livereload tools

```bash
heroku local:start -f Procfile_dev
```

### 7. Enjoy

```bash
open http://localhost:5000/
```

TODO: [make ready for prod deployment](https://docs.djangoproject.com/en/1.10/ref/django-admin/#cmdoption-check--deploy)
