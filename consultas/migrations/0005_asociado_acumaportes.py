# Generated by Django 4.2.7 on 2025-04-03 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0004_asociado_correo'),
    ]

    operations = [
        migrations.AddField(
            model_name='asociado',
            name='acumAportes',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
