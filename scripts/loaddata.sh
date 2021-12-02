#!/usr/bin/env bash
docker-compose exec django python manage.py loaddata sector5
docker-compose exec django python manage.py loaddata sector4
docker-compose exec django python manage.py loaddata sector3
docker-compose exec django python manage.py loaddata sector2
docker-compose exec django python manage.py loaddata plots
docker-compose exec django python manage.py loaddata section
docker-compose exec django python manage.py loaddata treatment
docker-compose exec django python manage.py loaddata inventory

