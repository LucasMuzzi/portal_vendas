import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Produto, Venda, Cliente, VendaProduto
from datetime import date
from django.db import transaction
from pymongo import MongoClient
from django.conf import settings

# Create your views here.


def pagina_vendas(request):
    context = {
        "today": date.today(),
    }
    return render(request, "vendas.html", context)


def buscar_produtos(request):
    ## Aqui eu vou resgatar o que foi solicitado pelo input
    termo_para_buscar = request.GET.get("term", "")

    ## Faço um filtro dentro do meu model de gerenciamento de produtos, buscando o que foi resgatado pelo input
    produtos = Produto.objects.filter(titulo__icontains=termo_para_buscar)

    ## Crio uma lista vazia para popular
    resultado = []

    ## Percorro no meu for os produtos resgatados, assim eu crio um JSON para poder popular com os dados
    for produto in produtos:
        resultado.append(
            {
                "id": produto.id,
                "titulo": produto.titulo,
                "descricao": produto.descricao,
                "preco": str(produto.preco),
                "fornecedor": produto.fornecedor,
                "imagem_url": produto.imagem.url if produto.imagem else "",
            }
        )

    ## Retorno o JSON
    return JsonResponse(resultado, safe=False)


def registrar_venda(request):
    ## Verifico qual foi o método de requisição do meu form.
    if request.method == "POST":

        # Resgato o valor de todos os inputs
        cliente_nome = request.POST.get("cliente")
        data_venda = request.POST.get("data")
        cep = request.POST.get("cep")
        rua = request.POST.get("rua")
        numero = request.POST.get("numero")
        bairro = request.POST.get("bairro")
        cidade = request.POST.get("cidade")
        estado = request.POST.get("estado")
        produtos_json = request.POST.get("produtos_json")

        # Valido se algo está faltando
        if not all(
            [
                cliente_nome,
                data_venda,
                cep,
                rua,
                numero,
                bairro,
                cidade,
                estado,
                produtos_json,
            ]
        ):
            messages.error(request, "Preencha todos os campos obrigatórios.")

            context = {"today": date.today()}
            return render(request, "vendas.html", context)

        try:
            ## Aqui começo a transação para poder gravar no postgres
            with transaction.atomic():

                # Resgato o json dos produtos
                produtos = json.loads(produtos_json)

                # Valido se há pelo menos um produto, caso não, retorno um erro para o front-end
                if not produtos:
                    messages.error(request, "Adicione pelo menos um produto à venda.")
                    context = {"today": date.today()}
                    return render(request, "vendas.html", context)

                # Se deu certo, crio o cliente caso não exista
                cliente, _ = Cliente.objects.get_or_create(nome=cliente_nome)

                # Faço o mesmo para minha tabela de venda, que registra os dados do endereço
                venda = Venda.objects.create(
                    cliente=cliente,
                    data=data_venda,
                    cep=cep,
                    rua=rua,
                    numero=numero,
                    bairro=bairro,
                    cidade=cidade,
                    estado=estado,
                )

                # Faço um for para percorrer os produtos que recebi no JSON, assim posso gravar todos os itens que foram vendidos
                for item in produtos:
                    produto_obj = Produto.objects.get(id=item["id"])
                    quantidade = item["quantidade"]
                    VendaProduto.objects.create(
                        venda=venda, produto=produto_obj, quantidade=quantidade
                    )

            try:
                # Aqui começo a validação no meu mongoDB, a ideia é gravar um snapshot do momento da venda..

                # Inicio a conexão no mongoDB
                client = MongoClient(settings.MONGO_URI)
                db = client[settings.MONGO_DATABASE_NAME]
                collection = db["vendas"]

                # Crio o objeto que vou poupular a tabela
                venda_documento = {
                    "venda_id_postgres": venda.id,
                    "cliente": cliente_nome,
                    "data_venda": data_venda,
                    "endereco_entrega": {
                        "cep": cep,
                        "rua": rua,
                        "numero": numero,
                        "bairro": bairro,
                        "cidade": cidade,
                        "estado": estado,
                    },
                    "produtos": produtos,
                    "total_venda": sum(
                        float(item["preco"]) * item["quantidade"] for item in produtos
                    ),
                }

                # Faço o insert na tabela
                collection.insert_one(venda_documento)
                # Encerro a conexão do mongoDB
                client.close()

            except Exception as e:
                # Caso haja alguma excessão, trato com um print aqui
                print(
                    f"AVISO: A venda foi salva no PostgreSQL, mas falhou ao salvar no MongoDB: {e}"
                )

            # Se tudo certo, vou registrar a venda e direcionar novamente para a pagina, permitindo outra venda
            messages.success(request, "Venda registrada com sucesso!")
            return redirect("vendas")

        except Exception as e:
            # Trato aqui caso ocorra um erro na transação
            messages.error(request, "Ocorreu um erro inesperado ao salvar a venda.")

            context = {"today": date.today()}
            return render(request, "vendas.html", context)

    return redirect("vendas")
