# Generated by Django 4.0.6 on 2022-08-11 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_ordemservico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='funcionario',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ordemservico',
            name='status',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]