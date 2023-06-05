from datetime import timedelta
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.


class Queja(models.Model):
    numero = models.IntegerField(auto_created=True, default=1, editable=False)
    nombre_apellidos = models.CharField(max_length=50)
    entidadAfectada = models.CharField(max_length=50)
    modalidad = models.CharField(max_length=50)
    via = models.CharField(max_length=50)
    procedencia = models.CharField(max_length=50)
    clasificacion = models.CharField(max_length=50)
    casoPrensa = models.CharField(max_length=50)
    fechaR = models.DateTimeField()
    fechaT = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    orden = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'queja'
        verbose_name_plural = 'quejas'

    def __str__(self):
        texto = 'numero: {}....Nombre y Apellidos: {}.... Fecha Recibido: {}'
        return texto.format(self.numero, self.nombre_apellidos, self.fechaR.date())

    def save(self, *args, **kwargs):
        if not self.pk:
            last_number = Queja.objects.filter(fechaR__year=self.fechaR.year).order_by('-numero').first()
            if last_number:
                self.numero = last_number.numero + 1
            else:
                self.numero = 1
        super().save(*args, **kwargs)


class Respuesta(models.Model):
    numero = models.OneToOneField(Queja, on_delete=models.CASCADE, related_name='respuesta')
    responsable = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=1000)
    entrega = models.BooleanField(default=False)
    satisfaccion = models.CharField(max_length=50, blank=True)
    conclusion = models.CharField(max_length=50, blank=True)
    fechaE = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'respuesta'
        verbose_name_plural = 'respuestas'

    def __str__(self):
        azucar = 'Queja: {} Responsable: {} Entrega: {} '
        return azucar.format(self.numero, self.responsable, self.entrega)


@receiver(pre_save, sender=Queja)
def actualizar_fecha_termino(sender, instance, **kwargs):
    if instance.fechaR:
        instance.fechaT = instance.fechaR + timedelta(days=30)