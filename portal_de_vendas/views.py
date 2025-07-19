import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Produto, Venda, Cliente, VendaProduto
from datetime import date
from django.db import transaction
from pymongo import MongoClient
from django.conf import settings
from datetime import datetime
from django.urls import reverse

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

    if request.method == "POST":

        # Coleta de dados
        cliente_nome = request.POST.get("cliente")
        cliente_email = request.POST.get("cliente_email")
        data_venda = request.POST.get("data")
        cep = request.POST.get("cep")
        rua = request.POST.get("rua")
        numero = request.POST.get("numero")
        bairro = request.POST.get("bairro")
        cidade = request.POST.get("cidade")
        estado = request.POST.get("estado")
        produtos_json = request.POST.get("produtos_json")

        if numero == "":
            numero = None

        if not all(
            [
                cliente_nome,
                cliente_email,
                data_venda,
                cep,
                rua,
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

            with transaction.atomic():

                produtos = json.loads(produtos_json)
                if not produtos:

                    messages.error(request, "Adicione pelo menos um produto à venda.")
                    context = {"today": date.today()}
                    return render(request, "vendas.html", context)

                cliente, criado = Cliente.objects.update_or_create(
                    email=cliente_email, defaults={"nome": cliente_nome}
                )

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

                for item in produtos:
                    produto_obj = Produto.objects.get(id=item["id"])
                    quantidade = item["quantidade"]
                    VendaProduto.objects.create(
                        venda=venda, produto=produto_obj, quantidade=quantidade
                    )

            try:

                client = MongoClient(settings.MONGO_URI)
                db = client[settings.MONGO_DATABASE_NAME]
                collection = db["vendas"]

                venda_documento = {
                    "venda_id_postgres": venda.id,
                    "cliente": {"nome": cliente_nome, "email": cliente_email},
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

                collection.insert_one(venda_documento)
                client.close()

            except Exception as e:
                print(f"!!! AVISO: Falha ao salvar no MongoDB: {e} !!!")

            messages.success(request, "Venda registrada com sucesso!")
            return redirect("vendas")

        except Exception as e:

            messages.error(request, "Ocorreu um erro inesperado ao salvar a venda.")
            context = {"today": date.today()}
            return render(request, "vendas.html", context)

    return redirect("vendas")


def historico_vendas(request):
    vendas_historico = []
    cliente_email = request.GET.get("email", None)

    query = {}
    if cliente_email:
        query = {"cliente.email": cliente_email}

    try:
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.MONGO_DATABASE_NAME]

        vendas_cursor = db["vendas"].find(query).sort("_id", -1)

        for venda in vendas_cursor:
            venda["id_str"] = str(venda["_id"])
            venda["produtos"] = venda.get("produtos", [])
            data_str = venda.get("data_venda", "")
            if data_str:
                data_obj = datetime.strptime(data_str, "%Y-%m-%d")
                venda["data_venda_formatada"] = data_obj.strftime("%d/%m/%Y")
            else:
                venda["data_venda_formatada"] = "N/A"
            vendas_historico.append(venda)

        client.close()
    except Exception as e:
        print(f"ERRO AO BUSCAR HISTÓRICO NO MONGODB: {e}")
        messages.error(request, "Não foi possível carregar o histórico de vendas.")

    context = {
        "vendas": vendas_historico,
        "cliente_email": cliente_email,
    }
    return render(request, "historico.html", context)


def buscar_historico_cliente(request):
    if request.method == "POST":
        cliente_email = request.POST.get("cliente_email")

        if Cliente.objects.filter(email=cliente_email).exists():

            base_url = reverse("historico_vendas")
            query_string = f"?email={cliente_email}"
            return redirect(base_url + query_string)
        else:
            messages.error(request, "Nenhum cliente encontrado com este e-mail.")
            return redirect("login")

    return redirect("login")
