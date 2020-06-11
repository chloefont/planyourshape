# Projet perso muscu

## Installation

If you don't have Pipenv already, install it :
```bash
pip3 install pipenv
```

Clone the repository :
```bash
git clone git@gitlab.liip.ch:chloefont/projet-perso-muscu
```

Create yourself a superuser :
```bash
pipenv run python manage.py createsuperuser
```

Run the project :
```bash
pipenv run python manage.py runserver
```


## Running tests

Run your tests :
```bash
pipenv run python manage.py test
```
