from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from .models import Service
from .serializers import ServiceSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'descricao', 'tags', 'prestador__first_name', 'prestador__last_name']

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_prestador', False):
            # Prestador vê só seus serviços
            return Service.objects.filter(prestador=user)
        # Clientes e outros veem todos os serviços
        return Service.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if not getattr(user, 'is_prestador', False):
            raise PermissionDenied("Apenas prestadores podem criar serviços.")
        serializer.save(prestador=user)

    def perform_update(self, serializer):
        user = self.request.user
        service = self.get_object()
        if service.prestador != user:
            raise PermissionDenied("Você só pode editar seus próprios serviços.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if instance.prestador != user:
            raise PermissionDenied("Você só pode deletar seus próprios serviços.")
        instance.delete()
