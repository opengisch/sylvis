#!/usr/bin/env bash

# create demo data
docker-compose exec django python manage.py loaddata sector5 sector4 sector3 sector2 plots section treatment inventory
docker-compose exec django python manage.py rebuild_sectors_tree  # rebuild mptt-tree
docker-compose exec django python manage.py updatedata  # recompute computed fields

# create default groups and users (admin//test, manager//test, worker//test)
docker-compose exec django python manage.py loaddata demo_users
