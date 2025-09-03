from django.contrib import admin
from .models import Product, ProductImages,Address,Query

class ProductImagesInline(admin.TabularInline):  
    model = ProductImages
    extra = 1 
    fields = ['images']
    max_num = 10 

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline]
    list_display = ['name', 'category', 'mrp', 'offprice', 'rating', 'itemtype', 'color']

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages)
admin.site.register(Address)
admin.site.register(Query)

