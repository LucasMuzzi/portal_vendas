import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Produto, Cliente, Venda, VendaProduto, Fornecedor


class ProdutoModelTest(TestCase):

    def test_criacao_de_produto_e_metodo_str(self):
        fornecedor_obj = Fornecedor.objects.create(nome="Fornecedor de Teste")

        produto = Produto.objects.create(
            titulo="Produto de Teste",
            preco=123.45,
            fornecedor=fornecedor_obj,
        )

        self.assertEqual(produto.titulo, "Produto de Teste")
        self.assertEqual(produto.preco, 123.45)

        self.assertEqual(produto.fornecedor.nome, "Fornecedor de Teste")

        self.assertEqual(str(produto), "Produto de Teste")


class ProdutoApiTest(TestCase):

    def setUp(self):

        fornecedor_x = Fornecedor.objects.create(nome="Fornecedor X")
        fornecedor_y = Fornecedor.objects.create(nome="Fornecedor Y")

        Produto.objects.create(
            titulo="Sensor de Teste A", preco=100.00, fornecedor=fornecedor_x
        )
        Produto.objects.create(
            titulo="Monitor de Teste B", preco=250.50, fornecedor=fornecedor_y
        )

    def test_busca_encontra_produto_existente(self):

        url = reverse("buscar_produto")
        response = self.client.get(url, {"term": "Sensor"})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["titulo"], "Sensor de Teste A")
        self.assertEqual(data[0]["fornecedor"], "Fornecedor X")

    def test_busca_nao_encontra_produto_inexistente(self):

        url = reverse("buscar_produto")
        response = self.client.get(url, {"term": "ProdutoInexistente"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)


class RegistrarVendaViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="vendedor_teste", password="senha_super_segura"
        )
        self.fornecedor = Fornecedor.objects.create(nome="Fornecedor Padrão")
        self.produto1 = Produto.objects.create(
            titulo="Produto Teste Venda", preco=50.00, fornecedor=self.fornecedor
        )

    def test_registrar_venda_com_sucesso(self):
        self.client.login(username="vendedor_teste", password="senha_super_segura")

        produtos_no_carrinho = [
            {
                "id": self.produto1.id,
                "titulo": self.produto1.titulo,
                "preco": float(self.produto1.preco),
                "quantidade": 2,
                "fornecedor": self.fornecedor.nome,
            }
        ]
        dados_da_venda = {
            "cliente": "Cliente Teste Final",
            "cliente_email": "teste@email.com",
            "data": "2025-07-21",
            "cep": "12345678",
            "rua": "Rua de Teste",
            "numero": "123",
            "bairro": "Bairro Teste",
            "cidade": "Cidade Teste",
            "estado": "SP",
            "produtos_json": json.dumps(produtos_no_carrinho),
        }

        url = reverse("registrar_venda")
        response = self.client.post(url, dados_da_venda)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("vendas"))

        self.assertEqual(Cliente.objects.count(), 1)
        self.assertEqual(Venda.objects.count(), 1)
        self.assertEqual(VendaProduto.objects.count(), 1)

        venda_salva = Venda.objects.first()
        item_vendido = VendaProduto.objects.first()
        self.assertEqual(venda_salva.cliente.nome, "Cliente Teste Final")
        self.assertEqual(venda_salva.cliente.email, "teste@email.com")
        self.assertEqual(item_vendido.produto.titulo, "Produto Teste Venda")
        self.assertEqual(item_vendido.quantidade, 2)
