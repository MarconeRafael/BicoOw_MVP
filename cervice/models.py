from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_proposta', 'Em Proposta'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    cep = models.CharField(max_length=9)  # formato "00000-000"
    endereco = models.CharField(max_length=255)
    prestador = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='services_provided')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.cliente}"

class Proposal(models.Model):
    service = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='proposals')
    prestador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals_made')
    mensagem = models.TextField()
    preco_proposto = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposta de {self.prestador} para {self.service}"
