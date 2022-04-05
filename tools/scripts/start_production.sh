#!/bin/sh

NAME="booking_core"                      # name of the application
DJANGODIR=/code/booking_core             # Django project directory
NUM_WORKERS=3                             # number of Gunicorn worker processes
DJANGO_WSGI_MODULE=booking_core.wsgi     # WSGI module name
# The maximum number of requests a worker will process before restarting. Limit the damage of memory leaks.
GUNICORN_MAX_REQUESTS=2000
BIND=0.0.0.0:8080
TIMEOUT=120
LOG_LEVEL="ERROR"
LOG_FORMAT="%(h)s %(l)s %(u)s %(t)s [GUNICORN] \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\""

sh /code/tools/scripts/wait_for_database.sh
python manage.py migrate
python manage.py collectstatic --no-input

echo "# Starting $NAME as `whoami` with $DJANGO_SETTINGS_MODULE and loglevel = $LOG_LEVEL - workers $NUM_WORKERS"

# start your Django Unicorn
# programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  -k gthread \
  --name ${NAME} \
  --max-requests ${GUNICORN_MAX_REQUESTS} \
  --workers ${NUM_WORKERS} \
  --timeout ${TIMEOUT} \
  --bind ${BIND} \
  --log-level ${LOG_LEVEL} \
  --log-file "-" \
  --access-logformat "${LOG_FORMAT}" \
  --access-logfile "-" \
  --error-logfile "-"
