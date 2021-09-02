# Opengis.ch Geodjango template

This is a template repository to serve as a base for building Geodjango projects.

It consists of a sample Django project with a docker compose setup.

It should work on any system that runs a recent version of Docker.


## Quickstart

```
# Clone the repository
git clone https://github.com/opengisch/template-geodjango.git -o template myproject

# Enter in the directory
cd myproject

# Start the stack
docker compose up --build -d

# Create a superuser
docker compose exec django python manage.py createsuperuser
```

After a while, you should be able to access `http://localhost:8000/admin` in your browser.

To completely remove the stack (including all data !)
```
# THIS DELETES ALL DATA !
docker compose down --volume
```

## Configuration

The basic configuration of the docker compose stack are in `.env`.


## Typical development cycle

1. Make some to the model definition in `src/myapp/models.py` (and `src/myapp/admin.py`)
3. Create the according migrations using `docker compose exec django python manage.py makemigrations`
4. Inspect the generated migration script under `src/myapp/migrations/XXXX.py`
5. Migrate the database using `docker compose exec django python manage.py migrate`

Note that the setup includes auto-reload, so that Django reloads automatically whenever you do some changes to the code.

To add other apps, run `docker compose exec django python manage.py startapp yourapp`, then add `yourapp` in the `INSTALLED_APPS` list of `src/settings.py`.


## Typical deployment

```
docker compose -f docker-compose.yml up --build -d
```

Ensure you're somehow backing up the postgres database and the media_volume !!


## Code style

We recommend using the provided pre-commit setup that will ensure consistent coding style. Enable with like this :
```
pip install pre-commit
pre-commit install
```


## Possible improvements to the template

- [ ] Use `pip-tools` (or similar) to pin python requirements, ensuring that deployements are deterministic.
- [ ] Include Caddy to provide https encryption and serve static files (instead of using --insecure)
- [ ] Include VSCode config for code completion/live debugging.
- [ ] Include Github actions to run tests.
- [ ] Run using gunicorn (or similar) on production instead of live dev server.
