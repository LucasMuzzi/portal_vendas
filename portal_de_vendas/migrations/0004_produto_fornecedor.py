# Generated by Django 4.2 on 2025-07-19 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_de_vendas', '0003_cliente_venda_vendaproduto_venda_produtos'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='fornecedor',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Fornecedor'),
        ),
    ]
