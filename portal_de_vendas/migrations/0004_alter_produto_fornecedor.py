# Generated by Django 4.2 on 2025-07-21 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal_de_vendas', '0003_fornecedor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='fornecedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='portal_de_vendas.fornecedor', verbose_name='Fornecedor'),
        ),
    ]
