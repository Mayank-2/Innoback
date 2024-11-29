from django.contrib import admin
from .models import User , Profile


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')

admin.site.register(Profile)