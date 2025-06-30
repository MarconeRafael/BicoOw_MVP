from django.urls import path
from .views import ServiceListView, service_detail, ProposalCreateView

app_name = 'cervice'

urlpatterns = [
    path('requests/', ServiceListView.as_view(), name='service_list'),
    path('requests/<int:id>/', service_detail, name='service_detail'),
    path('requests/<int:id>/propose/', ProposalCreateView.as_view(), name='propose'),
]
