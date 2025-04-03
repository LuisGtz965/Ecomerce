from decimal import Decimal
from django.conf import settings
from shop.models import Product


"""
CLASE CART - GESTIÓN DEL CARRITO DE COMPRAS

Implementa un carrito de compras persistente en sesión con:
- Almacenamiento de productos con cantidades y precios
- Cálculo automático de totales
- Métodos para añadir/remover/actualizar items
- Integración con modelos de productos existentes
"""

class Cart:
    def __init__(self, request):
        """
        Inicializa el carrito obteniendo la sesión actual.
        Si no existe carrito en sesión, crea uno vacío.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Crea un carrito vacío en la sesión
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Itera sobre los items del carrito obteniendo los productos 
        completos desde la base de datos.
        Calcula precios totales por item (precio x cantidad).
        """
        product_ids = self.cart.keys()
        # Obtiene los productos y los añade al carrito
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Retorna la cantidad total de items en el carrito
        (suma de todas las cantidades).
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Añade un producto al carrito o actualiza su cantidad.
        Args:
            product: Instancia del modelo Product
            quantity: Cantidad a añadir (default 1)
            override_quantity: Si True, reemplaza la cantidad en lugar de sumar
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                    'price': str(product.price)}
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()

    def save(self):
        """Marca la sesión como modificada para asegurar persistencia."""
        self.session.modified = True

    def remove(self, product):
        """
        Elimina un producto del carrito completamente.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """Vacía completamente el carrito eliminándolo de la sesión."""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        """
        Calcula el precio total sumando (precio x cantidad) de todos los items.
        Returns:
            Decimal: Total del carrito
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())