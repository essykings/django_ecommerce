from django.contrib import admin
from .models import Product,Cart

# admin.site.register(Product)

from django.utils.html import format_html
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'formatted_description', 'price')  # Customize list display

    def formatted_description(self, obj):
        return format_html(obj.description)  # This renders the HTML content

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)

