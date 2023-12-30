python -m venv venv
call venv/scripts/activate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 
