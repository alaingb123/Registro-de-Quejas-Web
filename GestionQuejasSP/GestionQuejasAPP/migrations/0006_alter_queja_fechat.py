# Generated by Django 4.2 on 2023-05-16 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionQuejasAPP', '0005_remove_respuesta_fechat_queja_fechat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queja',
            name='fechaT',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
