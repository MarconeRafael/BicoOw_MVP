from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import home_view
from django.contrib.auth.views import LogoutView


schema_view = get_schema_view(
    openapi.Info(
        title="BicoOw API",
        default_version='v1',
        description="API do MVP BicoOw - plataforma de bicos",
        contact=openapi.Contact(email="contato@bicoow.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Home (sem autenticação)
    path('', home_view, name='home'),

    # Admin
    path('admin/', admin.site.urls),

    # Auth JWT
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Apps com namespace
    path('api/users/', include('users.urls')),
    path('api/services/', include('cervice.urls')),  # assumindo que o app se chama 'cervice'
    path('api/appointments/', include('appointments.urls')),

    # Swagger / OpenAPI - corrigido para re_path com regex para json ou yaml
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # Logout (exemplo, se usar django.contrib.auth logout view)
    # path('logout/', LogoutView.as_view(), name='logout'), 
    # Se não usar logout por view, remova o link no template base.html
]
