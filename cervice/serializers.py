from rest_framework import serializers
from .models import ServiceRequest, Proposal
from django.conf import settings

User = settings.AUTH_USER_MODEL

class ProposalSerializer(serializers.ModelSerializer):
    prestador = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Proposal
        fields = ['id', 'service', 'prestador', 'mensagem', 'preco_proposto', 'created_at']
        read_only_fields = ['id', 'prestador', 'created_at']

class ServiceRequestSerializer(serializers.ModelSerializer):
    cliente = serializers.StringRelatedField(read_only=True)
    prestador = serializers.StringRelatedField(read_only=True)
    proposals = ProposalSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'cliente', 'titulo', 'descricao', 'cep', 'endereco',
            'prestador', 'status', 'created_at', 'proposals'
        ]
        read_only_fields = ['id', 'cliente', 'prestador', 'created_at', 'proposals']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['cliente'] = request.user
        return super().create(validated_data)
