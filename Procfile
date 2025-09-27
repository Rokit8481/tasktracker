web: cd tasker && python manage.py collectstatic --noinput && python manage.py migrate && gunicorn tasker.wsgi:application --bind 0.0.0.0:$PORT
