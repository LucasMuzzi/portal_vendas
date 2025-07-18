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
    imagem = models.ImageField(
        upload_to="produtos/", blank=True, null=True, verbose_name="Img Produto"
    )
    

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
