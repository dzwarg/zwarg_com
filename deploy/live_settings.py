
SECRET_KEY = "%(secret_key)s"
NEVERCACHE_KEY = "%(nevercache_key)s"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        # DB name or path to database file if using sqlite3.
        "NAME": "%(db_name)s",
        # Not used with sqlite3.
        "USER": "%(db_user)s",
        # Not used with sqlite3.
        "PASSWORD": "%(db_pass)s",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "%(db_host)s",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "%(db_port)s",
    }
}

ALLOWED_HOSTS = [
    "%(live_host)s"
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

CACHE_MIDDLEWARE_SECONDS = 60

CACHE_MIDDLEWARE_KEY_PREFIX = "%(proj_name)s"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

AWS_ACCESS_KEY_ID = "%(aws_id)s"
AWS_SECRET_ACCESS_KEY = "%(aws_key)s"
AWS_STORAGE_BUCKET_NAME = "%(aws_bucket)s"
STATIC_URL = 'http://{0}.s3.amazonaws.com/{1}/'.format(AWS_STORAGE_BUCKET_NAME, 'static')
MEDIA_URL = 'http://{0}.s3.amazonaws.com/{1}/'.format(AWS_STORAGE_BUCKET_NAME, 'media')
