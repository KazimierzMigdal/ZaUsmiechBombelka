from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='messages-home'),
    path('message/<int:pk>/', views.message_detail, name='messages_detail'),
    path('compose/<int:pk>/', views.compose, name='messages_compose'),
    path('message/delete/<int:pk>/', views.message_delete, name='message_delete'),
]
