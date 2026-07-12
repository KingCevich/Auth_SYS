web: gunicorn auth_serv.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate