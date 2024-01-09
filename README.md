pip freeze > requirements.txt


django-admin startproject apirest
python manage.py startapp accounts
python manage.py startapp products
python manage.py startapp cart
python manage.py startapp orders


python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations accounts
python manage.py migrate accounts
python manage.py makemigrations products
python manage.py migrate products
python manage.py makemigrations cart
python manage.py migrate cart
python manage.py makemigrations orders
python manage.py migrate orders


python manage.py createadmin

python manage.py runserver

lsof -i :8000
kill -9

pip install djangorestframework