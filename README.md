python -m venv .venv

pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install Pillow

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


{
  "product": {
    "id": 1,
    "quantity": 2
  }
}


Listar y crear órdenes: 

GET /api/orders/ y 
POST /api/orders/

Obtener, actualizar y eliminar una orden específica: 

GET /api/orders/<id>/, 
PUT /api/orders/<id>/ y 
DELETE /api/orders/<id>/

