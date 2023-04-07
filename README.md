# Helpdesk System

A system for managing a helpdesk.

## Production

In general, the [Django deployment guidelines](https://docs.djangoproject.com/en/4.2/howto/deployment/) should be followed.

If SRComp is live, you can sync teams and pit locations using a management command:

```bash
./manage.py import_from_srcomp --srcomp_url "https://srcomp.studentrobotics.org/comp-api"
```

## Development

This is a Django application.

1. Clone the repository
2. `python3 -m venv venv`
3. `source venv/bin/activate`
4. `pip3 install -r requirements-dev.txt`
5. `cd helpdesk`
6. `cp helpdesk/configuration.dev.py helpdesk/configuration.py`
7. `./manage.py migrate`
8. `./manage.py createsuperuser`
9. `./manage.py runserver`

The `Makefile` contains commands that can be used to run tests and linting:

- `make lint` - Lint
- `make test` - Run unit tests
- `make type` - Type checking

## SR2023 Deployment

This system was deployed for the helpdesk at the SR2023 competition as an experiment and received positive feedback. It was deployed on a 512MB 1 core machine on [Fly](https://fly.io) with a separate Postgres database server of the same specifications.