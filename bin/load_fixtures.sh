#!/bin/bash

python manage.py loaddata fixtures/public_site.json
python manage.py loaddata fixtures/public_site.content.json
python manage.py loaddata fixtures/public_site.teammember.json
python manage.py loaddata fixtures/public_site.partner.json
