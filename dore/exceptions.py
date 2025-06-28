from rest_framework.exceptions import APIException

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = "Serviço temporariamente indisponível. Tente novamente mais tarde."
    default_code = "service_unavailable"

class InvalidAppointmentTime(APIException):
    status_code = 400
    default_detail = "Horário do agendamento inválido."
    default_code = "invalid_appointment_time"

class PermissionDeniedCustom(APIException):
    status_code = 403
    default_detail = "Você não tem permissão para realizar esta ação."
    default_code = "permission_denied_custom"
