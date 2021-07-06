# Plan your shape

## Installation

This project is running in python 3.7.

If you don't have Pipenv already, install it :
```bash
> pip3 install pipenv
```

Clone the repository :
```bash
> git clone git@gitlab.liip.ch:chloefont/projet-perso-muscu
```

Install Django in your local folder :
```bash
> pipenv install "django<2.3"
```

Install the packages :
```bash
> pipenv install
> pipenv install --dev
```

Create yourself a superuser :
```bash
> pipenv run python manage.py createsuperuser
```

Run the project :
```bash
> pipenv run python manage.py runserver
```

## Running tests

Run your tests :
```bash
> pipenv run python manage.py test
```
