from django.db.models.signals import *
from django.dispatch import receiver
from project_management.models import *
from django.contrib.auth.models import User

# @receiver(post_save, sender= Project)
# def print_message(sender, instance, **kwargs):
#     print(sender.objects.get(instance).name + "has been created")
#     print(sender.objects.get(instance).user)

# from django.db.models.signals import post_delete

# @receiver(post_delete, sender=Project)
# def delete_notification(sender, instance, **kwargs):
#     name= instance.name
#     print(f"{name} has been deleted")

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, address='ktm', username='pawan', phone='9812345678', country='Nepal')
        print("Profile is created")
      


