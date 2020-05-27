release: python manage.py migrate
web: gunicorn velafrica.core.wsgi --timeout 60 --graceful-timeout 30 --log-level debug --log-file -
