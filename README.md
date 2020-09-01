# tracking.velafrica.ch

This project is an ERP (Enterprise resource planning) system for the people at Velafrica ( [http://velafrica.ch](http://velafrica.ch) ).
It consists of different modules, all serving the purpose to manage specific processes and teams inside Velafrica.

TODO: docker instructions

# Releases

We are using zest.releaser for version management.

https://zestreleaser.readthedocs.io/

Commands:

* prerelease
* release
* postrelease
* fullrelease

# Setup

## 1. Install required software

### python 3.6.1
- macOS: `brew install python3`
- Windows: download installer from https://www.python.org/downloads/release/python-361/

### python-pip
- macOs:
- Windows:

### pipenv
```bash
pip install pipenv
```

### Weasyprint dependencies
We use Weasyprint to generate PDF files.
Follow the installation instructions here: https://weasyprint.readthedocs.io/en/latest/install.html#

Weasyprint itself will be installed using pipenv in "Getting started".

- macOs:


    brew install cairo pango gdk-pixbuf libffi

If there are permission errors, make sure to give your user write access on /usr/local


    sudo chown -R $(whoami) /usr/local/*
   
   
### Postgres
- postgresql (9.4)

### NodeJS
node (5.5): https://nodejs.org/download/release/v5.5.0/

### Heroku Toolbelt
https://devcenter.heroku.com/articles/heroku-command-line#download-and-install

## Getting started

### 1. Setup virtual environment (pipenv)

<strong>NOTE:</strong> Before we were using virtualenv, but we migrated to pipenv recently, since it is easier to use and better supported by IDEs.

```bash
pipenv install --python 3.6
```

This creates a virtual environment.

### 2. Activate your virtual environment

```bash
pipenv shell
```

### 3. Define the environment variables

```bash
cp .env_dist .env
```

### 4. Add your database connection in the new .env file

Fill in your database credentials (eg. username, password & database name) in `.env`, by modifying the following entry: 

```bash
DATABASE_URL=postgres://your-username:your-password@localhost:5432/velafrica_dev
```

### 5. Create database (apply migrations)

```bash
heroku local:run python manage.py migrate
```

### 6. Compile the translation files

```bash
heroku local:run python manage.py compilemessages
```

### 7. Load the fixture data

```bash
heroku local:run ./bin/load_fixtures.sh
```


### 8. Start development server & livereload tools

```bash
heroku local:start -f Procfile_dev
```

### 9. Enjoy

```bash
open http://localhost:8000/
```

### (Optional)

```bash
# Export database to file
pg_dump -U <your-username> velafrica_dev > dbexport.pgsql

# Import database form file
psql -U <your-username> velafrica_dev < dbexport.pgsql

# Extract translations from the templates & code into a .po file
python manage.py makemessages -a \
-i node_modules \
-i staticfiles \
-i tmp \
-i venv
```

# Deployment

The instructions here are meant for a fresh deployment to heroku. For consecutive deployments, heroku and github are currently set up in a way that successful builds of the `master` branch trigger a deployment to heroku. The current configuration (`npm run postinstall` & the heroku release commands) make sure that the assets are being compiled and the schema migrations are applied.

```bash
# Create a new heroku application
heroku create <your-app-name> --region=eu

# Add a postgresql database
heroku addons:create heroku-postgresql:hobby-dev --app <your-app-name>

# Add rollbar to log errors in production
heroku addons:create rollbar:free --app <your-app-name>

# Set the debugging to false, to make sure we're not leaking information to the user in case of an error
heroku config:set DEBUG=False --app <your-app-name>

# Make sure all the required buildpacks are defined and the order is the same.
open https://dashboard.heroku.com/apps/<your-app-name>/settings

1st buildpack: https://github.com/heroku/heroku-buildpack-addon-wait
2nd buildpack: https://github.com/philippkueng/heroku-buildpack-sassc
3rd buildpack: heroku/nodejs
4th buildpack: heroku/python

# The deploy the code for the first time.
git push heroku master

# (Optional) setup automatic deployments
open https://dashboard.heroku.com/apps/<your-app-name>/deploy/github
```

# Fixtures
To update / save new fixtures run
```
heroku local:run python manage.py dumpdata --format=json --indent=2 -v 2 [app_name] | grep -v "Loaded ENV .env" > fixtures/[app_name].json
```
or for specific models:
```
heroku local:run python manage.py dumpdata --format=json --indent=2 -v 2 [app_name.model] | grep -v "Loaded ENV .env" > fixtures/[app_name.model].json
```
Before you commit the new fixtures file, make sure you remove dev/test data from the json and only commit those changes which are relevant for staging or production

# Documentation

Most of the classes should be documented. More documentation is available per request (chregi.glatthard (at) gmail.com).
