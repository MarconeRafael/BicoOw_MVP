from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import home_view

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

    # URLs baseadas em template do app users (login, logout, perfil, cadastro)
    path('', include('users.urls', namespace='users')),

    # Admin
    path('admin/', admin.site.urls),

    # Auth JWT
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # APIs dos apps
    path('api/users/', include('users.urls')),
    path('api/services/', include('cervice.urls')),
    path('api/appointments/', include('appointments.urls')),

    # Swagger / OpenAPI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', 
            schema_view.without_ui(cache_timeout=0), 
            name='schema-json'),
    path('swagger/', 
         schema_view.with_ui('swagger', cache_timeout=0), 
         name='schema-swagger-ui'),
    path('redoc/', 
         schema_view.with_ui('redoc', cache_timeout=0), 
         name='schema-redoc'),
]
