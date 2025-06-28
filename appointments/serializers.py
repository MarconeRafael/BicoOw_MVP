from rest_framework import serializers
from .models import Appointment
from cervice.models import Service
from cervice.serializers import ServiceSerializer
from users.serializers import UserSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    cliente = UserSerializer(read_only=True)
    prestador = UserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='service',
        write_only=True
    )
    prestador_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.none(),  # inicial vazio
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
        # Ajusta queryset de prestadores com base no service_id passado
        service_id = None
        if self.initial_data:
            service_id = self.initial_data.get('service_id') or self.initial_data.get('service')
        if service_id:
            try:
                service = Service.objects.get(pk=service_id)
                # Ajuste aqui para obter queryset de prestadores compatíveis com o serviço
                # Exemplo genérico:
                prestadores_qs = service.prestador.__class__.objects.filter(pk=service.prestador.pk)
                self.fields['prestador_id'].queryset = prestadores_qs
            except Service.DoesNotExist:
                self.fields['prestador_id'].queryset = Service.objects.none()
        else:
            self.fields['prestador_id'].queryset = Service.objects.none()
