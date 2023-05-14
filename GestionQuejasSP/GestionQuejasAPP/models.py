from django.db import models

# Create your models here.


class Queja(models.Model):
    numero=models.IntegerField(auto_created=True,default=1,editable=False)
    nombre_apellidos=models.CharField(max_length=20)
    entidadAfectada=models.CharField(max_length=20)
    modalidad=models.CharField(max_length=20)
    via=models.CharField(max_length=20)
    procedencia=models.CharField(max_length=20)
    clasificacion=models.CharField(max_length=20)
    casoPrensa=models.CharField(max_length=20)
    fechaR=models.DateTimeField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='queja'
        verbose_name_plural='quejas'

    def __str__(self):
        texto = 'numero: {} Nombre y Apellidos: {} Entidad Afectada: {} Fecha Recibida {}  '
        return texto.format(self.numero, self.nombre_apellidos, self.entidadAfectada,self.fechaR)

    def save( self,*args,**kwargs ):
        if not self.pk:
            last_number=Queja.objects.filter(fechaR__year=self.fechaR.year).order_by('-numero').first()
            if last_number:
                self.numero=last_number.numero + 1
        super().save(*args,**kwargs)


class Respuesta(models.Model):
    numero=models.OneToOneField(Queja,on_delete=models.CASCADE)
    responsable=models.CharField(max_length=20)
    descripcion=models.TextField(max_length=300)
    entrega=models.BooleanField
    satisfaccion=models.CharField(max_length=20)
    conclusion=models.CharField(max_length=20)
    fechaT=models.DateTimeField()
    fechaE=models.DateTimeField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='respuesta'
        verbose_name_plural='respuestas'

    def __str__(self):
        return self.numero,self.responsable,self.entrega,self.fechaT