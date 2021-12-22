from django.contrib import admin

# Register your models here.
from .models import Category,Product,Image

admin.site.register(Category)

class ImageInline(admin.StackedInline):
    model = Image


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_at')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ImageInline,]
    
admin.site.register(Product,ProductAdmin)

