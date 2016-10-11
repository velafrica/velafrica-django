release: bin/addon-wait && python manage.py migrate && npm run prod
web: gunicorn velafrica.core.wsgi --log-file -
