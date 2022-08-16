# Generated by Django 4.0.6 on 2022-08-11 23:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_ordemservico_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ordemservico',
            name='funcionario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='funcionario', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
