# Generated by Django 4.2 on 2023-05-14 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GestionQuejasAPP', '0002_remove_respuesta_numero_delete_queja_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Queja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(auto_created=True, default=1, editable=False)),
                ('nombre_apellidos', models.CharField(max_length=20)),
                ('entidadAfectada', models.CharField(max_length=20)),
                ('modalidad', models.CharField(max_length=20)),
                ('via', models.CharField(max_length=20)),
                ('procedencia', models.CharField(max_length=20)),
                ('clasificacion', models.CharField(max_length=20)),
                ('casoPrensa', models.CharField(max_length=20)),
                ('fechaR', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'queja',
                'verbose_name_plural': 'quejas',
            },
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responsable', models.CharField(max_length=20)),
                ('descripcion', models.TextField(max_length=300)),
                ('satisfaccion', models.CharField(max_length=20)),
                ('conclusion', models.CharField(max_length=20)),
                ('fechaT', models.DateTimeField()),
                ('fechaE', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('numero', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='GestionQuejasAPP.queja')),
            ],
            options={
                'verbose_name': 'respuesta',
                'verbose_name_plural': 'respuestas',
            },
        ),
    ]
