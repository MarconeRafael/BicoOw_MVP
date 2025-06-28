from django.db.models.signals import post_save
from django.dispatch import receiver
from appointments.models import Appointment

@receiver(post_save, sender=Appointment)
def notify_appointment_status(sender, instance, created, **kwargs):
    if created:
        # Simula notificação para prestador e cliente ao criar agendamento
        prestador = instance.prestador
        cliente = instance.cliente
        print(f"Notificação: Novo agendamento #{instance.id} criado entre {cliente.get_full_name()} e {prestador.get_full_name()}")
    else:
        # Notificação para atualização de status, por exemplo
        print(f"Notificação: Agendamento #{instance.id} atualizado para status {instance.status}")
