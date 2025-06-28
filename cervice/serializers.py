from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    prestador_nome = serializers.CharField(source='prestador.get_full_name', read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'prestador', 'prestador_nome', 'nome', 'descricao', 'valor_por_hora', 'tags', 'created_at', 'updated_at']
        read_only_fields = ['prestador', 'created_at', 'updated_at']
