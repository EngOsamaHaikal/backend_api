from django.contrib import admin

# Register your models here.
from .models import Category,Product ,Review ,Cart,CartItem

admin.site.register(Category)
admin.site.register(Cart)

admin.site.register(CartItem)

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