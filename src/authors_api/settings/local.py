from .base import * #noqa
from .base import env

SECRET_KEY = env("DJANGO_SECRET_KEY", 
                 default="oYBpGb6kBOZOoRURy8D4uDJNep4AE320spVr-rgppMIg2t2ZAxc",)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#list of domains allowed to make cross-site requests to the site, add this because we are goignt o use nginx
CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "marilynjmarquez@gmail.com"
DOMAIN = env("DOMAIN")
SITE_NAME="Authors Haven"



#to generate secret key: python -c "import secrets; print(secrets.token_urlsafe(38))"