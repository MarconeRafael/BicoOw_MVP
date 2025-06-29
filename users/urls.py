from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    login_view,
    logout_view,
    register_view,
    perfil_view,
    editar_perfil_view,
    RegisterView,
    UserListView,
    UserDetailView,
    consulta_cep,  # import da nova view
)

app_name = 'users'

urlpatterns = [
    # --- Views baseadas em template (HTML) ---
    path('login/', login_view, name='login_form'),
    path('logout/', logout_view, name='logout'),
    path('register-form/', register_view, name='register_form'),
    path('perfil/', perfil_view, name='user_profile'),
    path('perfil/editar/', editar_perfil_view, name='editar_perfil'),

    # --- Autenticação via API (JWT) ---
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # --- Views baseadas em API (DRF) ---
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/me/', UserDetailView.as_view(), name='user_detail'),
    path('api/', UserListView.as_view(), name='user_list'),

    # --- AJAX para consulta CEP ---
    path('ajax/consulta-cep/', consulta_cep, name='ajax_consulta_cep'),
]
