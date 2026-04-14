from django.urls import path
from .views import TicketListCreateAPIView, TicketDetailAPIView, HealthCheckAPIView

urlpatterns = [
    # Ticket CRUD endpoints
    path('tickets/', TicketListCreateAPIView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>/', TicketDetailAPIView.as_view(), name='ticket-detail'),
    
    # Health check endpoint
    path('health/', HealthCheckAPIView.as_view(), name='health-check'),
]
