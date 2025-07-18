from django.shortcuts import render

# Create your views here.


def pagina_vendas(request):
    return render(request, "vendas.html")
