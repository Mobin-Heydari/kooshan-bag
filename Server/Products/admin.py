from django.contrib import admin
from . import models


@admin.register(models.PrimeryCategory)
class PrimeryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['primery_category', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    
admin.site.register(models.Color)

admin.site.register(models.ProductImage)

admin.site.register(models.ProductDescription)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'slug', 'price',
        'quantity', 'available', 'created', 'updated'
    ]
    list_filter = ['available']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['colors', 'descriptions']
    filter_vertical = ['images']

