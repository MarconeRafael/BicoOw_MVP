from django.urls import path
from .views import (
    RegisterView, UserDetailView, UserListView,
    perfil_view, editar_perfil_view,
    login_view, register_view, logout_view
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'users'

urlpatterns = [
    # --- Autenticação via API (JWT) ---
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/me/', UserDetailView.as_view(), name='user_detail'),
    path('api/', UserListView.as_view(), name='user_list'),

    # --- Views baseadas em template (HTML) ---
    path('perfil/', perfil_view, name='user_profile'),
    path('perfil/editar/', editar_perfil_view, name='edit_profile'),
    path('login/', login_view, name='login_form'),
    path('register-form/', register_view, name='register_form'),
    path('logout/', logout_view, name='logout'),
]
