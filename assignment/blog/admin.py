from django.contrib import admin

from .models import Blog, Follow
# Register your models here.
admin.site.register(Blog)
admin.site.register(Follow)