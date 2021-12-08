# Sylvis prototype


## Quickstart

```
# Configure the stack
cp .env.example .env
nano .env

# Start the stack
docker compose up --build -d

# Restore initial data
./scripts/loaddata.sh
```

Note: initial data fixtures are not yet versionned. You must manually copy `sector5.json` `sector4.json` `sector3.json` `sector2.json` `plots.json` `section.json` `treatment.json` `inventory.json` to `src/sylvis/fixtures` for loaddata.sh to fully work.

After a while, you should be able to access `http://localhost` in your browser.

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


## Deployment


### Initial setup

Run the following step on the server (Ubuntu-20.04)
```
# Install docker, docker-compose and git
sudo apt update
sudo apt-get install -y docker.io docker-compose git
sudo usermod -aG docker $USER
sudo reboot 0

# Create a key pair
ssh-keygen -t ed25519 -C "system@sylvis.org"

# Add the contents of ~/.ssh/id_ed25519.pub as a deploy key in the Github repository

# Clone the git repository
git clone git@github.com:opengisch/sylvis.git

# Start the stack
cd sylvis
docker-compose -f docker-compose.yml up --build -d --remove-orphans
```

### Manual deployement

To deploy changes manually:
```
cd sylvis
git pull
docker-compose -f docker-compose.yml up --build -d --remove-orphans
```

### Automated deployement

Github CI will automatically deploy changes when a new release is created.

It requires the following secrets:
- `DEPLOY_SSH_PRIVATE_KEY`
- `DEPLOY_SSH_USER`
- `DEPLOY_SSH_HOST`
- `DEPLOY_SSH_PORT`

It is assumed the checkout repo is available under `./sylvis` for that SSH user, with a `.env` file
containing the deployment stack config.


## Translations

Translations are managed on the [Sylvis transifex project](https://www.transifex.com/opengisch/sylvis). New strings are pushed automatically with Github workflows, and translations are pulled in the entrypoint.

No manual steps should be required to have up to date translations, but for reference, here are the steps to push/pull translations:

```
# Push new strings to transifex
docker-compose exec -T django python manage.py makemessages -l en
docker-compose exec django tx push --source

# Pull translations from transifex
docker-compose exec -T django tx pull -a
docker-compose exec django python manage.py compilemessages
```

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
- [ ] Backup setup
