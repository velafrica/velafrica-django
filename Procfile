release: bin/addon-wait && yes | python manage.py migrate
web: gunicorn velafrica.core.wsgi --log-file -
