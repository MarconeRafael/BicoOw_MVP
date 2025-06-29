from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Cliente'),
        ('provider', 'Prestador'),
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='client',
    )

    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Foto principal do usuário

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class ClienteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente_profile')
    cep = models.CharField(max_length=9, blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Perfil do Cliente: {self.user.username}"


class PrestadorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='prestador_profile')
    cep = models.CharField(max_length=9, blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    especialidade = models.CharField(max_length=150, blank=True)
    experiencia = models.TextField(blank=True)
    tempo_atuacao_anos = models.PositiveIntegerField(null=True, blank=True)  # tempo de experiência em anos
    portfolio_url = models.URLField(blank=True)  # link para portfólio externo
    preco_hora = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # preço/hora
    disponibilidade = models.CharField(max_length=100, blank=True)  # exemplo: "Seg a Sex, 9h-18h"

    def __str__(self):
        return f"Perfil do Prestador: {self.user.username}"


class FotoPrestador(models.Model):
    prestador = models.ForeignKey(PrestadorProfile, on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='prestadores/fotos/')
    descricao = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Foto de {self.prestador.user.username}"


class Avaliacao(models.Model):
    prestador = models.ForeignKey(PrestadorProfile, on_delete=models.CASCADE, related_name='avaliacoes')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avaliacoes_feitas')
    nota = models.PositiveSmallIntegerField()  # nota entre 1 e 5
    comentario = models.TextField(blank=True)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('prestador', 'cliente')  # evita múltiplas avaliações do mesmo cliente

    def __str__(self):
        return f"Avaliação de {self.cliente.username} para {self.prestador.user.username}"
