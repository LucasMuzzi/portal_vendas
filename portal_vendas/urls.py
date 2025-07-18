from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from portal_de_vendas import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Rotas para login e logout
    path("", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("vendas/", views.pagina_vendas, name="vendas"),
]
