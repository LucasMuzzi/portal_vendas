from django.shortcuts import render
from django.http import JsonResponse
from .models import Produto

# Create your views here.


def pagina_vendas(request):
    return render(request, "vendas.html")


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
                "imagem_url": produto.imagem.url if produto.imagem else "",
            }
        )

    ## Retorno o JSON
    return JsonResponse(resultado, safe=False)
