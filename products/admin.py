from django.contrib import admin
from .models import Category, Brand, Product, Images, ProductAttachment
# Register your models here.

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Images)
admin.site.register(ProductAttachment)