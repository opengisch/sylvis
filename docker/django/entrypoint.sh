#!/bin/bash

set -e

# TODO: unsure it's good practice to do that here since
# failing transifex would prevent starting the container.
tx pull -a
python manage.py compilemessages

python manage.py collectstatic --no-input
python manage.py migrate --no-input

exec $@
