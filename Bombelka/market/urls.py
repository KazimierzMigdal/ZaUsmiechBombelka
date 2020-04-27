from django.urls import path
from . import views
from .views import (ProductCreateView,
                    ProductDetailView,
                    ProductUpdateView,
                    ProductDeleteView,
                    ProductSoldView)

urlpatterns = [
    path('', views.main, name='market-home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='product-delete'),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/sold', ProductSoldView.as_view(), name='product-sold'),
    path('product/new/', ProductCreateView.as_view(), name='product-create'),
    path('product/<username>/', views.user_products, name='user-products')
]
