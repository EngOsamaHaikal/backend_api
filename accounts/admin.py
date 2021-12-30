from django.contrib import admin
from .models import CustomUser,NewsSubscription
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(NewsSubscription)