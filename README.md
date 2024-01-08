# Cooking helper / продуктовый помощник
## Description:
Project foodgram-project-react is a cooking helper. It allows you to make and share recipes, follow other authors.
Make grocery lists out of recipes of your interest.

## How to run project in dev-mode locally
### Clone repository and access it through command line:
```
git clone git@github.com:RealTheOne/foodgram-project-react.git
cd foodgram-project-react
```
### Make sure that DATABASES in /backend/foodgram/settings.py:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
### In /infra/ run a command (You should have Docker and Docker Compose installed):
```
docker compose up
```
### In /backend/ install and activate local environment:
```
python -m venv venv
```
### In /backend/ install requirements and make migrations:
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```
### In /backend/ run project:
```
python manage.py runserver
```
### Access api in your browser:
```
http://127.0.0.1:8000/api
```
### Access frontend and docs in your browser:
```
http://localhost/
http://localhost/api/docs/
```

## stack
1. Python 3.9.10
2. Django 4.2.3
3. DRF
4. JWT + Djoser
5. NGinx
6. Gunicorn
7. React
8. Docker
 
## Author: 
 Idrisov Arthur
