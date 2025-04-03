from django import forms

"""
FORMULARIO PARA AÑADIR PRODUCTOS AL CARRITO

Define un formulario para seleccionar cantidades de productos con:
- Selector numérico de cantidades (1-20)
- Campo oculto para control de actualización de cantidades
"""
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)