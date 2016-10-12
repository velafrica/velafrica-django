release: bin/addon-wait && python manage.py migrate
web: gunicorn velafrica.core.wsgi --log-file -
