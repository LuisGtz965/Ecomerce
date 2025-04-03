from django.urls import path
from . import views
"""
CONFIGURACIÓN DE URLs PARA LA APLICACIÓN CARRITO

Define las rutas para operaciones del carrito de compras con estructura RESTful:
- Ruta base: /cart/
- Rutas nombradas para fácil referencia en templates
- Captura de ID de producto en URLs para acciones específicas
"""
app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    # Añadir/actualizar producto (POST)
    # URL: /cart/add/<product_id>/
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    # Eliminar producto (POST)
    # URL: /cart/remove/<product_id>/
    path('remove/<int:product_id>/', views.cart_remove,
                                     name='cart_remove'),
]