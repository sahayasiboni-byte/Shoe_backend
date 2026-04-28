from django.contrib import admin

# Register your models here.
from .models import img, products
admin.site.register(img)
admin.site.register(products)