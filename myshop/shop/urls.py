from django.urls import path
from . import views

"""
Define las rutas principales del sistema de e-commerce con:
- Vista de mapa interactivo
- Listados de productos (general y por categoría)
- Vista detallada de productos
"""

app_name = 'shop'

urlpatterns = [
    path('mapa/', views.mapa, name='mapa'),  
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
]