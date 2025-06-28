from django.urls import path
from .views import RegisterView, UserDetailView, UserListView, perfil_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserDetailView.as_view(), name='user_detail'),

    # Listagem de usuários na raiz /api/users/
    path('', UserListView.as_view(), name='user_list'),

    # Rota para a página do perfil do usuário (template HTML)
    path('perfil/', perfil_view, name='user_profile'),
]
