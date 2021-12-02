#!/usr/bin/env bash
docker-compose exec django python manage.py loaddata sector5 sector4 sector3 sector2 plots section treatment inventory
docker-compose exec django python manage.py rebuild_sectors_tree
