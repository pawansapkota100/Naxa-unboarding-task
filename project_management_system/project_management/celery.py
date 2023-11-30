import os

from celery import Celery


# set environment default so project settings.py is accessible using DJANGO_SETTINGS_MODULE key
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_management_system.settings")

# initialize the celery app
# And pass the module where celery.py is defined. In our case it is week1
app = Celery("project_management")

# in settings.py of the project, The configuration for celery start with CELERY.
# so celery config setting looks like CELERY_BACKEND_URL
app.config_from_object("django.conf:settings", namespace="CELERY")


# it will automatically discover the task from the apps in the projects
app.autodiscover_tasks()


