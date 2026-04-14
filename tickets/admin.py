from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Ticket model.
    
    Provides a clean interface for managing tickets in Django admin.
    """
    list_display = ('title', 'status', 'priority', 'requester_name', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'description', 'requester_name', 'requester_email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
