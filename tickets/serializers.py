from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ticket model.
    
    Converts Ticket model instances to JSON format for the API
    and validates incoming data when creating/updating tickets.
    """
    
    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'requester_name',
            'requester_email',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_title(self, value):
        """Ensure title is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()
