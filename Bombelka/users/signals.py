from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Contact
from django.db.models.signals import m2m_changed



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Contact)
def users_followers_changed_3(sender, instance, **kwargs):
    instance.user_to.total_followers = instance.user_to.followers.count()
    instance.user_to.save()

@receiver(pre_delete, sender=Contact)
def users_followers_changed_4(sender, instance, **kwargs):
    instance.user_to.total_followers = instance.user_to.total_followers - 1
    instance.user_to.save()
