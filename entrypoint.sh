#!/bin/sh

python3 manage.py collectstatic --no-input \
    && python3 manage.py migrate \
    && python3 manage.py seed \
    && gunicorn course_checkout_poc.wsgi:application --bind 0.0.0.0:8000