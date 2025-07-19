from django.db import models


# Create your models here.
class Produto(models.Model):
    titulo = models.CharField(
        max_length=200, verbose_name="Título", null=False, blank=False
    )
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    preco = models.DecimalField(
        max_digits=20, decimal_places=2, null=False, blank=False
    )
    fornecedor = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Fornecedor"
    )
    imagem = models.ImageField(
        upload_to="produtos/", blank=True, null=True, verbose_name="Img Produto"
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"


class Cliente(models.Model):
    nome = models.CharField(max_length=100)


class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateField()
    cep = models.CharField(max_length=8)
    rua = models.CharField(max_length=100)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    produtos = models.ManyToManyField(Produto, through="VendaProduto")


class VendaProduto(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
