# Generated by Django 4.2 on 2025-07-18 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal_de_vendas', '0002_rename_prdouto_produto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('cep', models.CharField(max_length=8)),
                ('rua', models.CharField(max_length=100)),
                ('numero', models.IntegerField()),
                ('bairro', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=2)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal_de_vendas.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='VendaProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal_de_vendas.produto')),
                ('venda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal_de_vendas.venda')),
            ],
        ),
        migrations.AddField(
            model_name='venda',
            name='produtos',
            field=models.ManyToManyField(through='portal_de_vendas.VendaProduto', to='portal_de_vendas.produto'),
        ),
    ]
