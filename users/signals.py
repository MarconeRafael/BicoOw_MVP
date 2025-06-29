from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import User, ClienteProfile, PrestadorProfile

@receiver(post_save, sender=User)
def criar_perfil_automaticamente(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'client':
            ClienteProfile.objects.create(user=instance)
        elif instance.user_type == 'provider':
            PrestadorProfile.objects.create(user=instance)
