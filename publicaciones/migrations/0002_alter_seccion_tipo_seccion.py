# Generated by Django 3.2 on 2023-11-05 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicaciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seccion',
            name='tipo_seccion',
            field=models.CharField(choices=[('Articulo', 'Articulo'), ('Noticia', 'Noticia'), ('Galeria', 'Galeria'), ('About', 'About')], max_length=10),
        ),
    ]
