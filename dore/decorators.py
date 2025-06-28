from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def log_access(func):
    """
    Decorador simples para logar chamadas de funções/views.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Acessando função {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def require_json_content_type(func):
    """
    Decorador para garantir que a requisição tenha Content-Type: application/json.
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.content_type != 'application/json':
            return Response({"detail": "Content-Type deve ser application/json."}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        return func(request, *args, **kwargs)
    return wrapper
