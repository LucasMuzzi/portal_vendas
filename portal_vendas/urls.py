from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from portal_de_vendas import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # Rotas para login e logout
    path("", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    ## Rotas para a pagina de vendas
    path("vendas/", views.pagina_vendas, name="vendas"),
    path("buscar-produto/", views.buscar_produtos, name="buscar_produto"),
    path("registrar-venda/", views.registrar_venda, name="registrar_venda"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
