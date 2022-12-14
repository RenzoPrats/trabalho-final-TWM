# Generated by Django 4.0.6 on 2022-08-11 22:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_carro_tiposeguro'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdemServico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=500, verbose_name='Descrição')),
                ('data', models.DateField(auto_now_add=True)),
                ('funcionario', models.IntegerField()),
                ('relatorio', models.CharField(max_length=500, verbose_name='Relatório')),
                ('status', models.IntegerField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tiposeguro')),
            ],
        ),
    ]
