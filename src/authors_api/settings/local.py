from .base import * #noqa
from .base import env

SECRET_KEY = env("DJANGO_SECRET_KEY", 
                 default="oYBpGb6kBOZOoRURy8D4uDJNep4AE320spVr-rgppMIg2t2ZAxc",)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#list of domains allowed to make cross-site requests to the site, add this because we are goignt o use nginx
CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]



#to generate secret key: python -c "import secrets; print(secrets.token_urlsafe(38))"