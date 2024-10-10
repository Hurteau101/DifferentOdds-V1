release: python manage.py migrate
web: gunicorn DifferentOdds.wsgi --log-file -
worker: celery -A DifferentOdds worker --pool solo --loglevel=info
beat: celery -A DifferentOdds beat --loglevel=info