from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Deportes(models.Model):
    #Deporte_ID GENERADO POR DJANGO
    descripcion = models.CharField(db_column='Descripcion',max_length=40)

    class Meta:
        db_table            = 'deportes'
        ordering            = ['descripcion']
        verbose_name        = 'Deporte'
        verbose_name_plural = 'Deportes'

    def __str__(self) -> str:
        return self.descripcion
        #return super().__str__()

class Predios(models.Model):
    #Predio_ID GENERADO POR DJANGO
    user_id   = models.ForeignKey(User, models.PROTECT, db_column='user_id',verbose_name='User ID')
    nombre    = models.CharField (db_column='Nombre',max_length=50,null=False)
    direccion = models.CharField (db_column='Direccion',max_length=250,null=True,blank=True)
    lat       = models.FloatField(db_column='lat',blank=True,null=True)
    lng       = models.FloatField(db_column='lng',blank=True,null=True)

    class Meta:
        db_table            = 'predios'
        ordering            = ['nombre']
        verbose_name        = 'Predio'
        verbose_name_plural = 'Predios'
    
    def __str__(self) -> str:
        # super().__str__()
        return self.nombre

class Canchas(models.Model):
    #Cancha_ID GENERADO POR DJANGO
    predio_id   = models.ForeignKey(Predios, models.PROTECT, db_column='predio_id',verbose_name='Predio ID')
    deporte_id  = models.ForeignKey(Deportes, models.PROTECT, db_column='deporte_id',verbose_name='Deporte ID')
    nombre      = models.CharField (db_column='Nombre',max_length=50,null=False)
    foto        = models.ImageField(upload_to='upload/',db_column='Foto')#, null=True)#(db_column='Foto',max_length=250)
    precio      = models.FloatField (db_column='Precio')#,null=True,blank=True)
    anticipo    = models.FloatField(db_column='Anticipo')#,blank=True,null=True)
    

    class Meta:
        db_table            = 'canchas'
        ordering            = ['nombre']
        verbose_name        = 'Cancha'
        verbose_name_plural = 'Canchas'
    
    def __str__(self) -> str:
        # super().__str__()
        return self.predio_id.nombre+' | '+ self.nombre

class Reservas(models.Model):
    #Reserva_ID GENERADO POR DJANGO
    user_id   = models.ForeignKey   (User, models.PROTECT, db_column='user_id',verbose_name='User ID')
    cancha_id = models.ForeignKey   (Canchas,models.PROTECT,db_column='cancha_id')
    fecha_ini = models.DateTimeField(db_column='Fecha_Ini',null=False,blank=False)
    fecha_fin = models.DateTimeField(db_column='Fecha_Fin',null=False,blank=False)
    precio    = models.FloatField (db_column='Precio')#,null=True,blank=True)
    anticipo  = models.FloatField(db_column='Anticipo')#,blank=True,null=True)

    class Meta:
        db_table            = 'reservas'
        ordering            =['id']#,'reservas_id']
        verbose_name        = 'Reserva'
        verbose_name_plural = 'Reservas'
    
    def __str__(self) -> str:
        #return super().__str__()
        return str(self.fecha_ini) + ' hasta ' + str(self.fecha_fin)

class Roles(models.Model):
    descripcion = models.CharField(db_column='Descripcion',max_length=40)

    class Meta:
        db_table            = 'roles'
        ordering            = ['descripcion']
        verbose_name        = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self) -> str:
        return self.descripcion
        #return super().__str__()
        
class UsuarioXRoles(models.Model):
    user_id = models.ForeignKey(User,models.PROTECT,db_column='user_id',verbose_name='User ID')
    rol_id  = models.ForeignKey(Roles,models.PROTECT,db_column='rol_id',verbose_name='Rol')

    class Meta:
        db_table            = 'usuario_roles'
        ordering            = ['user_id']
        verbose_name        = 'Rol usuario'
        verbose_name_plural = 'Roles de usuarios'

    def __str__(self) -> str:
        #return super().__str__()
        return str(self.user_id)+ ' - '+str(self.rol_id)

