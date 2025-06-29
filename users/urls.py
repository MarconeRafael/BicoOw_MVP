from django.urls import path
from .views import RegisterView, UserDetailView, UserListView, perfil_view, editar_perfil_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'users'  
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserDetailView.as_view(), name='user_detail'),
    path('', UserListView.as_view(), name='user_list'),

    path('perfil/', perfil_view, name='user_profile'),
    path('perfil/editar/', editar_perfil_view, name='edit_profile'),
]
