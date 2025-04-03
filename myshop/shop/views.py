from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product

"""
VISTAS PARA LA APLICACIÓN SHOP

Controladores que manejan:
1. Listado de productos (general/filtrado por categoría)
2. Vista detallada de productos con formulario para carrito
3. Mapa interactivo con manejo de coordenadas
"""
def product_list(request, category_slug=None):
    """
    Muestra listado de productos disponibles, con opción de filtrado por categoría.
    
    Args:
        request: HttpRequest object
        category_slug (str, optional): Slug de categoría para filtrar. Defaults to None.
    
    Returns:
        HttpResponse: Renderiza template con contexto:
            - category: Categoría actual (None si es listado general)
            - categories: Todas las categorías para el menú
            - products: Productos filtrados por disponibilidad y categoría
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request,
                'shop/product/list.html',
                {
                    'category': category,
                    'categories': categories,
                    'products': products
                })


def product_detail(request, id, slug):
    """
    Muestra vista detallada de un producto específico con formulario para añadir al carrito.
    
    Args:
        request: HttpRequest object
        id (int): ID del producto
        slug (str): Slug del producto para URLs SEO-friendly
    
    Returns:
        HttpResponse: Renderiza template con:
            - product: Producto obtenido por ID y slug
            - cart_product_form: Formulario para modificar cantidad en carrito
    """
    product = get_object_or_404(Product,
                              id=id,
                              slug=slug,
                              available=True)
    cart_product_form = CartAddProductForm()
    
    return render(request,
                'shop/product/detail.html',
                {
                    'product': product,
                    'cart_product_form': cart_product_form
                })


def mapa(request):
    """
    Vista para mapa interactivo con manejo de coordenadas:
    - Valida coordenadas recibidas por POST
    - Establece valores por defecto si hay errores
    - Pasa coordenadas al template para renderizar mapa
    
    Returns:
        HttpResponse: Renderiza template con:
            - lat: Latitud (valor por defecto o enviado por formulario)
            - lon: Longitud (valor por defecto o enviado por formulario)
    """
    # Coordenadas predeterminadas (Chihuahua, México)
    DEFAULT_COORDS = {
        'lat': 28.6408325,
        'lon': -106.1485902
    }
    
    lat = DEFAULT_COORDS['lat']
    lon = DEFAULT_COORDS['lon']

    if request.method == 'POST':
        try:
            # Conversión y validación básica
            lat = float(request.POST.get('lat', lat))
            lon = float(request.POST.get('lon', lon))
            
            # Validación de rangos geográficos
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValueError("Coordenadas fuera de rango válido")
                
        except (ValueError, TypeError) as e:
            # Fallback a valores por defecto y registro de error
            print(f"Error en coordenadas: {str(e)}")
            lat, lon = DEFAULT_COORDS.values()

    return render(request, 'map.html', {
        'lat': lat,
        'lon': lon
    })