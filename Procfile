release: bin/addon-wait && yes | python manage.py migrate
web: gunicorn velafrica.core.wsgi --timeout 50 --graceful-timeout 50 --log-file -
