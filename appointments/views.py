from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import ValidationError
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['cliente__first_name', 'prestador__first_name', 'service__nome', 'status']
    ordering_fields = ['data_hora_inicio', 'status']

    def get_queryset(self):
        user = self.request.user
        # Clientes veem só seus agendamentos como cliente
        # Prestadores veem só seus agendamentos como prestador
        if getattr(user, 'is_cliente', False):
            return Appointment.objects.filter(cliente=user)
        elif getattr(user, 'is_prestador', False):
            return Appointment.objects.filter(prestador=user)
        return Appointment.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        data_inicio = serializer.validated_data.get('data_hora_inicio')
        data_fim = serializer.validated_data.get('data_hora_fim')

        if data_fim <= data_inicio:
            raise ValidationError({"data_hora_fim": "A data e hora final devem ser posteriores à inicial."})

        # Aqui pode adicionar outras validações, ex: conflito de horário, disponibilidade do prestador etc.

        # Força cliente logado como cliente do agendamento
        serializer.save(cliente=user)
