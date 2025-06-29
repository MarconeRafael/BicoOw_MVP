# users/urls_templates.py
from django.urls import path
from .views import perfil_view, editar_perfil_view, login_view, register_view, logout_view

app_name = 'users'
urlpatterns = [
    path('perfil/', perfil_view, name='user_profile'),
    path('perfil/editar/', editar_perfil_view, name='edit_profile'),
    path('login/', login_view, name='login_form'),
    path('logout/', logout_view, name='logout'),
    path('register-form/', register_view, name='register_form'),
]
