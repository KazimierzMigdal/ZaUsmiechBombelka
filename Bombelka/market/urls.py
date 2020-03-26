from django.urls import path
from . import views
from .views import (ProductCreateView,
                    ProductListView,
                    ProductDetailView,
                    ProductUpdateView,
                    ProductDeleteView)

urlpatterns = [
    path('', ProductListView.as_view(), name='market-home'),
    path('product/new/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<username>/', views.user_products, name='user-products'),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='product-delete')
]
