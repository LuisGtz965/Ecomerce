from django.db import models
from django.urls import reverse

"""
MODELOS PRINCIPALES PARA SISTEMA DE E-COMMERCE

Define la estructura de datos para categorías y productos con:
- Relaciones Many-to-One (Productos → Categoría)
- URLs amigables (SlugField)
- Optimización para consultas (índices)
- Métodos para generación de URLs absolutas
"""

class Category(models.Model):
    """
    Modelo para categorías de productos:
    - Campos básicos: nombre y slug (URL única)
    - Métodos para representación y navegación
    """
    name = models.CharField(max_length=200)  # Nombre de la categoría
    slug = models.SlugField(max_length=200, unique=True)  # Versión para URL

    class Meta:
        ordering = ['name']  # Orden por defecto
        indexes = [
            models.Index(fields=['name']),  # Índice para búsquedas por nombre
        ]
        verbose_name = 'category'  # Nombre singular en admin
        verbose_name_plural = 'categories'  # Nombre plural en admin

    def __str__(self):
        return self.name  # Representación legible

    def get_absolute_url(self):
        """Genera URL para listado de productos por categoría"""
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    """
    Modelo para productos del catálogo:
    - Relación con categoría (borrado en cascada)
    - Campos para información básica y multimedia
    - Control de disponibilidad y fechas
    """
    category = models.ForeignKey(
        Category,
        related_name='products',  # Acceso inverso: category.products.all()
        on_delete=models.CASCADE  # Borrar productos si se elimina categoría
    )
    name = models.CharField(max_length=200)  # Nombre del producto
    slug = models.SlugField(max_length=200)  # Versión para URL
    image = models.ImageField(
        upload_to='products/%Y/%m/%d',  # Ruta organizada por fecha
        blank=True  # Opcional
    )
    description = models.TextField(blank=True)  # Descripción detallada
    price = models.DecimalField(
        max_digits=10,  # Máximo 10 dígitos
        decimal_places=2  # 2 decimales para moneda
    )
    available = models.BooleanField(default=True)  # Control de stock
    created = models.DateTimeField(auto_now_add=True)  # Fecha creación
    updated = models.DateTimeField(auto_now=True)  # Fecha última modificación

    class Meta:
        ordering = ['name']  # Orden por defecto
        indexes = [
            models.Index(fields=['id', 'slug']),  # Índice compuesto
            models.Index(fields=['name']),  # Índice para búsquedas
            models.Index(fields=['-created']),  # Índice ordenado por fecha (nuevos primero)
        ]

    def __str__(self):
        return self.name  # Representación legible

    def get_absolute_url(self):
        """Genera URL para vista detallada del producto"""
        return reverse('shop:product_detail', args=[self.id, self.slug])