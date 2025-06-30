from rest_framework import generics, permissions
from django.shortcuts import render, get_object_or_404, redirect
from .models import ServiceRequest, Proposal
from .serializers import ServiceRequestSerializer, ProposalSerializer
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

# API Views

class ServiceListView(generics.ListAPIView):
    """
    Lista as solicitações de serviço com status 'aberto' (visível para prestadores)
    """
    queryset = ServiceRequest.objects.filter(status='aberto').order_by('-created_at')
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProposalCreateView(generics.CreateAPIView):
    """
    Criar proposta para um serviço
    """
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Define o prestador automaticamente como o usuário autenticado
        serializer.save(prestador=self.request.user)


# Views baseadas em template

@login_required
@require_http_methods(["GET", "POST"])
def service_detail(request, id):
    service = get_object_or_404(ServiceRequest, pk=id)
    user = request.user

    if request.method == 'POST':
        # Recebe dados da proposta via formulário
        mensagem = request.POST.get('mensagem', '').strip()
        preco_proposto = request.POST.get('preco_proposto', '').strip()

        if not mensagem or not preco_proposto:
            # Pode implementar mensagens de erro aqui
            return render(request, 'cervice/service_detail.html', {
                'service': service,
                'error': 'Mensagem e preço são obrigatórios.'
            })

        try:
            preco_decimal = float(preco_proposto.replace(',', '.'))
        except ValueError:
            return render(request, 'cervice/service_detail.html', {
                'service': service,
                'error': 'Preço inválido.'
            })

        Proposal.objects.create(
            service=service,
            prestador=user,
            mensagem=mensagem,
            preco_proposto=preco_decimal
        )
        # Redireciona ou mostra sucesso
        return redirect('cervice:service_detail', id=service.id)

    return render(request, 'cervice/service_detail.html', {'service': service})
