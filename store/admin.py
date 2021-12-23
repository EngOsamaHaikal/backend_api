from django.contrib import admin

# Register your models here.
from .models import Category,Product ,Review

admin.site.register(Category)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'stock', 'available', 'image']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    list_filter = ("status",)
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    
admin.site.register(Product,ProductAdmin)

admin.site.register(Review)