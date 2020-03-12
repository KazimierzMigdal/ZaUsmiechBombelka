from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.db.models.signals import m2m_changed



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(m2m_changed, sender=User.followers.through)
def users_followers_changed(sender, instance, **kwargs):
    instance.total_followers = instance.followers.count()
    instance.save()


