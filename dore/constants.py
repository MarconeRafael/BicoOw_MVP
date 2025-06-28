from enum import Enum

class UserRole(str, Enum):
    CLIENTE = "cliente"
    PRESTADOR = "prestador"

class AppointmentStatus(str, Enum):
    PENDENTE = "PENDENTE"
    ACEITO = "ACEITO"
    CANCELADO = "CANCELADO"
    CONCLUIDO = "CONCLUIDO"

# Exemplos de tags padrões (podem ser usadas em serviços)
DEFAULT_SERVICE_TAGS = [
    "limpeza",
    "jardinagem",
    "babá",
    "consertos",
    "fretes",
    "reparos",
]
