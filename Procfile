release: python manage.py collectstatic --noinput
web: daphne -b 0.0.0.0 -p $PORT djangochat.asgi:application
