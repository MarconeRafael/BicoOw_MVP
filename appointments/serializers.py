from rest_framework import serializers
from .models import Appointment
from cervice.models import ServiceRequest
from cervice.serializers import ServiceRequestSerializer
from users.serializers import UserSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    cliente = UserSerializer(read_only=True)
    prestador = UserSerializer(read_only=True)
    service = ServiceRequestSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceRequest.objects.all(),
        source='service',
        write_only=True
    )
    prestador_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceRequest.objects.none(),  # inicial vazio
        source='prestador',
        write_only=True
    )

    class Meta:
        model = Appointment
        fields = [
            'id',
            'cliente',
            'prestador',
            'prestador_id',
            'service',
            'service_id',
            'data_hora_inicio',
            'data_hora_fim',
            'status',
            'criado_em',
            'atualizado_em',
        ]
        read_only_fields = ['id', 'cliente', 'status', 'criado_em', 'atualizado_em']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        service_id = None
        if self.initial_data:
            service_id = self.initial_data.get('service_id') or self.initial_data.get('service')
        if service_id:
            try:
                service = ServiceRequest.objects.get(pk=service_id)
                # Exemplo genérico: filtra prestadores com perfil provider (ajuste conforme sua regra)
                from users.models import User
                prestadores_qs = User.objects.filter(user_type='provider')
                self.fields['prestador_id'].queryset = prestadores_qs
            except ServiceRequest.DoesNotExist:
                self.fields['prestador_id'].queryset = User.objects.none()
        else:
            from users.models import User
            self.fields['prestador_id'].queryset = User.objects.none()
