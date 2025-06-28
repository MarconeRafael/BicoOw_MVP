from rest_framework import exceptions

class QuerysetByUserMixin:
    """
    Filtra queryset para que cada usuário veja só os objetos relacionados a ele.
    Pressupõe que o model tem um campo 'user' ou 'owner' ou similar.
    Para usar, defina `user_field` na view, ex: user_field = 'cliente' ou 'prestador'.
    """

    user_field = 'user'  # padrão, sobrescreva na view

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            raise exceptions.NotAuthenticated()
        filter_kwargs = {self.user_field: user}
        return qs.filter(**filter_kwargs)


class CustomPageNumberPaginationMixin:
    """
    Mixin para usar paginação personalizada (exemplo: página padrão e tamanho customizado).
    Deve ser usado junto com uma classe de paginação customizada definida em settings ou na view.
    """

    pagination_class = None  # defina sua paginação aqui ou no settings

    def paginate_queryset(self, queryset):
        if self.pagination_class is None:
            return None
        paginator = self.pagination_class()
        return paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        paginator = self.pagination_class()
        return paginator.get_paginated_response(data)
