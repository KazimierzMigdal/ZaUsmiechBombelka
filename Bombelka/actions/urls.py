from django.urls import path
from . import views


urlpatterns = [
    path('', views.actions, name='actions'),
]
