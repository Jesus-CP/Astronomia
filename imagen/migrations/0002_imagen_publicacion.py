# Generated by Django 3.2 on 2023-10-18 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('publicaciones', '0001_initial'),
        ('imagen', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagen',
            name='publicacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='publicaciones.publicacion'),
        ),
    ]
