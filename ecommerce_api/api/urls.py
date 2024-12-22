from django.urls import path
from . import views

urlpatterns = [
    # User Endpoints
    path('users/', views.user_list),
    path('users/<int:pk>/', views.user_detail),

    # Product Endpoints
    # path('products/', views.product_list),
    # path('products/<int:pk>/', views.product_detail),
]
