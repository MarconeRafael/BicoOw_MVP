from django.db import models
from django.conf import settings

class Service(models.Model):
    prestador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services'
    )
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    valor_por_hora = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.CharField(max_length=200, blank=True)  # Pode ser uma string separada por vírgulas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nome} - {self.prestador.get_full_name()}'
