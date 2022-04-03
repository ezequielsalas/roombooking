import environ

env = environ.Env(
    # Django
    SECRET_KEY=(str, ''),
    DEBUG=(bool, False),
    POSTGRES_HOST=(str, None),
    POSTGRES_DB=(str, None),
    POSTGRES_NAME=(str, None),
    POSTGRES_USER=(str, None),
    POSTGRES_PASSWORD=(str, None),
    POSTGRES_PORT=(int, 5432),
    ALLOWED_HOSTS=(list, []),
    STATIC_URL=(str, "/static/"),
    # Django storages
    DJANGO_DEFAULT_FILE_STORAGE=(str, ''),
    DJANGO_STATICFILES_STORAGE=(str, ''),
    DJANGO_SETTINGS_FILE=(str, 'booking_core.prod_settings'),
    # Celery
    REDIS_HOST=(str, 'redis://redis:6379'),
    CELERY_BROKER_URL=(str, 'redis://redis:6379/0'),
    CELERY_RESULT_BACKEND=(str, 'redis://redis:6379/0'),
)
