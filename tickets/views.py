from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from django.conf import settings

from .models import Ticket
from .serializers import TicketSerializer


class TicketListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating tickets.
    
    GET /api/tickets/ - List all tickets (with Redis caching)
    POST /api/tickets/ - Create a new ticket
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    
    def get(self, request, *args, **kwargs):
        """
        List all tickets with Redis caching.
        
        Checks cache first - if not found, queries database
        and stores result in Redis for future requests.
        """
        # Create a cache key based on query parameters
        cache_key = 'ticket_list'
        
        # Try to get from cache first
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)
        
        # Not in cache - get from database
        response = super().get(request, *args, **kwargs)
        
        # Cache the response for CACHE_TTL seconds (5 minutes)
        cache.set(cache_key, response.data, settings.CACHE_TTL)
        
        return response
    
    def post(self, request, *args, **kwargs):
        """
        Create a new ticket.
        
        Clears the ticket list cache after creation to ensure
        the next list request includes the new ticket.
        """
        response = super().post(request, *args, **kwargs)
        
        # Clear cache when new ticket is created
        cache.delete('ticket_list')
        
        return response


class TicketDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a single ticket.
    
    GET /api/tickets/<id>/ - Retrieve a ticket
    PUT /api/tickets/<id>/ - Update a ticket (full update)
    PATCH /api/tickets/<id>/ - Partial update a ticket
    DELETE /api/tickets/<id>/ - Delete a ticket
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    
    def perform_update(self, serializer):
        """
        Update the ticket and clear the cache.
        
        This handles both PUT (full update) and PATCH (partial update).
        """
        serializer.save()
        # Clear cache when ticket is updated
        cache.delete('ticket_list')
    
    def perform_destroy(self, instance):
        """
        Delete the ticket and clear the cache.
        """
        instance.delete()
        # Clear cache when ticket is deleted
        cache.delete('ticket_list')


class HealthCheckAPIView(APIView):
    """
    Health check endpoint for monitoring.
    
    GET /health/ - Check if the API is running properly
    
    Returns status of the application and database connectivity.
    """
    def get(self, request):
        health_data = {
            'status': 'healthy',
            'service': 'Django Ticket Manager API',
        }
        
        # Check database connectivity
        try:
            from django.db import connection
            connection.ensure_connection()
            health_data['database'] = 'connected'
        except Exception as e:
            health_data['status'] = 'unhealthy'
            health_data['database'] = f'error: {str(e)}'
        
        # Check Redis connectivity
        try:
            from django.core.cache import cache
            cache.set('health_check', 'ok', 10)
            result = cache.get('health_check')
            health_data['redis'] = 'connected' if result == 'ok' else 'error'
        except Exception as e:
            health_data['status'] = 'unhealthy'
            health_data['redis'] = f'error: {str(e)}'
        
        status_code = status.HTTP_200_OK if health_data['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
        
        return Response(health_data, status=status_code)
