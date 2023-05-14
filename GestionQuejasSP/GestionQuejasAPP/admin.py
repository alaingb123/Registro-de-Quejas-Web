from django.contrib import admin

from .models import Queja,Respuesta
# Register your models here.

class Queja_Admin(admin.ModelAdmin):
    readonly_fields = ('created','updated')
admin.site.register(Queja,Queja_Admin)

class Respuesta_Admin(admin.ModelAdmin):
    readonly_fields = ('created','updated')
admin.site.register(Respuesta,Respuesta_Admin)