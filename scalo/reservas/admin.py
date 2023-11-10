from django.contrib import admin
from reservas.models import Deportes,Predios,Roles,Canchas,Reservas,UsuarioXRoles,usuarios

# Register your models here.
#USER admin
#PW   admin
class CanchasAdmin(admin.ModelAdmin):
    list_display    = ['id','predio_id','nombre','foto','precio','anticipo']
    readonly_fields = ['id']
    search_fields   = ['nombre']
    actions         = None

admin.site.register(Canchas,CanchasAdmin)

class ReservasAdmin(admin.ModelAdmin):
    list_display    = ['id','user_id','cancha_id','fecha_ini','fecha_fin']
    readonly_fields = ['id']
    search_fields   = ['user_id']
    actions         = None

admin.site.register(Reservas,ReservasAdmin)

class RolesAdmin(admin.ModelAdmin):
    list_display    = ['id','descripcion']
    readonly_fields = ['id']
    search_fields   = ['descripcion']
    actions         = None

admin.site.register(Roles,RolesAdmin)

class UsuarioXRolesAdmin(admin.ModelAdmin):
    list_display    = ['id','user_id','rol_id']
    readonly_fields = ['id']
    search_fields   = ['user_id','rol_id']
    actions         = None

admin.site.register(UsuarioXRoles,UsuarioXRolesAdmin)

class PrediosAdmin(admin.ModelAdmin):
    list_display    = ['id','user_id','nombre','direccion','lat','lng','logo']
    readonly_fields = ['id']
    search_fields   = ['user_id','nombre','direccion']
    actions         = None

admin.site.register(Predios,PrediosAdmin)

class DeportesAdmin(admin.ModelAdmin):
    list_display    = ['id','descripcion']
    readonly_fields = ['id']
    search_fields   = ['user_id','descripcion']
    actions         = None




class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'fec_nac', 'telef', 'fecha_verificacion')
    search_fields = ('user_id__username', 'fec_nac', 'telef')
    
admin.site.register(usuarios,UsuariosAdmin)
