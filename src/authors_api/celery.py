import os 
from celery import Celery
from django.conf import settings

#TODO: change in production
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "authors_api.settings.local")

#Name celery instance:
app = Celery("authors_api")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) #automaticaly finds tasks in all installed Django applications