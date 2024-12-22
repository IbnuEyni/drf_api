from django.urls import path
from .views_2 import product_list, product_detail

urlpatterns = [
    path('products/', product_list, name='v2_product_list'),
    path('products/<int:pk>/', product_detail, name='v2_product_detail'),
]
