from django.db import models
from django.conf import settings
from cervice.models import ServiceRequest  # Ajuste para o novo model

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('ACEITO', 'Aceito'),
        ('CANCELADO', 'Cancelado'),
        ('CONCLUIDO', 'Concluído'),
    ]

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments_cliente'
    )
    prestador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments_prestador'
    )
    service = models.ForeignKey(
        ServiceRequest,            # Alterado aqui
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data_hora_inicio']

    def __str__(self):
        return f'Agendamento {self.id} - {self.cliente.get_full_name()} com {self.prestador.get_full_name()} - {self.status}'
