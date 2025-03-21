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
2. `python3 -m venv venv` (using Python 3.11)
3. `source venv/bin/activate`
4. `pip3 install -r requirements-dev.txt`
5. `cd helpdesk`
6. `./manage.py migrate`
7. `./manage.py createsuperuser`
8. `./manage.py runserver`

The `Makefile` contains commands that can be used to run tests and linting:

- `make lint` - Lint
- `make test` - Run unit tests
- `make type` - Type checking

## Deployment

This system is deployed using our [Ansible](https://github.com/srobo/ansible/) configuration.

### Login with Google

Credentials are configured through the Django admin. OAuth credentials need to be configured as below:

- User type: Internal (this ensures it's only SR accounts which can be used)
- Scopes: `.../auth/userinfo.email`, `.../auth/userinfo.profile`, `openid`
- Redirect URIs: `https://studentrobotics.org/helpdesk/auth/google/login/callback/`
- Authorised JavaScript origins: `https://studentrobotics.org`

A [project](https://console.cloud.google.com/home/dashboard?project=helpdesk-419320) exists for this in our Google Cloud account.
