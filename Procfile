release: python manage.py migrate
web: gunicorn velafrica.core.wsgi --timeout 30 --graceful-timeout 30 --log-level debug --log-file -
worker1: celery worker -A velafrica.core.celery
