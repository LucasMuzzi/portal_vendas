# Generated by Django 4.2 on 2025-07-19 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_de_vendas', '0005_cliente_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='numero',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
