from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['name', 'passwd']

@admin.register(Image)
class AdminImage(admin.ModelAdmin):
    readonly_fields = (id, )

@admin.register(ImageProcessing)
class AdminImageProcessing(admin.ModelAdmin):
    list_display = ['mask_size', 'brightness']

