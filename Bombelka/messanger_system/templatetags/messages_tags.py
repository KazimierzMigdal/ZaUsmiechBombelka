from django import template
from ..models import Message
from django.db.models import Q


register = template.Library()

@register.simple_tag(takes_context=True)
def new_messages(context):
    request = context['request']
    new_messages_counter = 0
    user = request.user
    new_messages_counter =  Message.objects.filter(
        Q(recipient=user)&Q(new=True)
        ).count()
    return new_messages_counter
