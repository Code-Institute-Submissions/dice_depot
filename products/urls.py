from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('<int:product_id>', views.product_description, name='product_description'),
    path('<add_product>', views.add_product, name='add_product'),
]