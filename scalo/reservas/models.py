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
    user_id     = models.ForeignKey(User, models.PROTECT, db_column='user_id',verbose_name='User ID')
    nombre      = models.CharField (db_column='Nombre',max_length=50,null=False)
    direccion   = models.CharField (db_column='Direccion',max_length=250)
    logo        = models.ImageField(upload_to='upload/',db_column='Foto')#, null=True)#(db_column='Foto',max_length=250)
    lat         = models.FloatField(db_column='lat',blank=True,null=True)
    lng         = models.FloatField(db_column='lng',blank=True,null=True)
    telefono    = models.CharField(max_length=15, db_column='Telefono', blank=True, null=True)  
    email       = models.EmailField(max_length=100, db_column='Email', blank=True, null=True)
    descripcion = models.CharField(max_length=100, db_column='Desripcion', blank=True, null=True)
    link_mapa   = models.CharField(max_length=1000, db_column='link_mapa', blank=True, null=True)
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

    ESTADO_RESERVA = (
        ('Cancelado', 'Cancelado'),
        ('Pendiente', 'Pendiente'),
        ('Activo', 'Activo'),
        ('Si_jugo', 'Si_jugo'),
        ('No_jugo', 'No_jugo'),
    )

    #Reserva_ID GENERADO POR DJANGO
    user_id   = models.ForeignKey   (User, models.PROTECT, db_column='user_id',verbose_name='User ID')
    cancha_id = models.ForeignKey   (Canchas,models.PROTECT,db_column='cancha_id')
    fecha_ini = models.DateTimeField(db_column='Fecha_Ini',null=False,blank=False)
    fecha_fin = models.DateTimeField(db_column='Fecha_Fin',null=False,blank=False)
    precio    = models.FloatField (db_column='Precio')#,null=True,blank=True)
    anticipo  = models.FloatField(db_column='Anticipo')#,blank=True,null=True)
    estado  = models.CharField(db_column='estado',max_length=20,choices=ESTADO_RESERVA, default='Pendiente')
    #idpago


    class Meta:
        db_table            = 'reservas'
        ordering            =['id']#,'reservas_id']
        verbose_name        = 'Reserva'
        verbose_name_plural = 'Reservas'
    
    def __str__(self) -> str:
        #return super().__str__()
        #return str(self.fecha_ini) + ' hasta ' + str(self.fecha_fin)
        return str(self.pk)

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

class usuarios(models.Model):
    user_id = models.ForeignKey(User,models.PROTECT,db_column='user_id',verbose_name='User ID')
    fec_nac = models.DateField(db_column='fec_nac', verbose_name="Fecha de nacimiento")
    telef   = models.CharField(db_column='telefono',max_length=11,verbose_name="Teléfono")

    class Meta:
        db_table            = 'usuarios'
        ordering            = ['user_id']
        verbose_name        = 'Datos de usuario'
        verbose_name_plural = 'Datos de usuarios'

    def __str__(self) -> str:
        #return super().__str__()
        return str(self.user_id)

class pagos(models.Model):
    #id
    payment_id = models.CharField(max_length=25, db_column='payment_id', blank=True, null=True)  
    status  = models.CharField(max_length=15, db_column='status', blank=True, null=True)  
    monto = models.FloatField (db_column='monto')#,null=True,blank=True)
    reserva_id = models.ForeignKey(Reservas,models.PROTECT,db_column='reserva_id',)

    class Meta:
        db_table            = 'pagos'
        #ordering            = ['user_id']
        verbose_name        = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self) -> str:
        #return super().__str__()
        return str(self.payment_id)