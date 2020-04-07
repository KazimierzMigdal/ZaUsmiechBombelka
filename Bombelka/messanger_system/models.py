from market.models import Product
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
    subject = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    sender = models.ForeignKey(User, related_name='sent_messages',on_delete=models.PROTECT)
    recipient = models.ForeignKey(User, related_name='received_messages', null=True, blank=True, on_delete=models.SET_NULL)
    sent_at = models.DateTimeField(default=timezone.now)
    new = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    parent_msg = models.ForeignKey('self', related_name='next_messages', null=True, blank=True, default=None, verbose_name="Parent message", on_delete=models.SET_NULL)


    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('messages_detail', kwargs={'pk': self.pk})
