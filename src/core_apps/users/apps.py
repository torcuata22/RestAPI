from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _ #allows for translation if you want to


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.users"
    verbose_name = _("Users") #creates singular, readable, for plural use: verbose_name_plural 
    
