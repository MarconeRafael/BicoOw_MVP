from rest_framework import permissions

class IsPrestador(permissions.BasePermission):
    """
    Permite acesso somente a usuários com papel de prestador.
    Pressupõe que User model tem atributo booleano is_prestador.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'is_prestador', False))


class IsCliente(permissions.BasePermission):
    """
    Permite acesso somente a usuários com papel de cliente.
    Pressupõe que User model tem atributo booleano is_cliente.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'is_cliente', False))


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permite edição apenas ao dono do objeto (objeto deve ter atributo 'owner' ou 'user').
    Outros podem apenas ler.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, 'owner', None) or getattr(obj, 'user', None)
        return owner == request.user
