from django.apps import AppConfig
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in

class SupplierConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'supplier'
