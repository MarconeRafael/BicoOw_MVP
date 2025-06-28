from rest_framework import generics, permissions, filters
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def perfil_view(request):
    user = request.user
    return render(request, 'users/perfil.html', {'user': user})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # só admin pode listar todos usuários
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']

    def get_queryset(self):
        queryset = super().get_queryset()
        user_type = self.request.query_params.get('type')
        if user_type == 'cliente':
            queryset = queryset.filter(is_cliente=True)
        elif user_type == 'prestador':
            queryset = queryset.filter(is_prestador=True)
        return queryset

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
