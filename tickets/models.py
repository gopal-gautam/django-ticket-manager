from django.db import models


class Ticket(models.Model):
    """
    IT Support Ticket Model
    
    Represents a support ticket in the IT ticket management system.
    Each ticket has a status, priority level, and requester information.
    """
    
    # Status choices for tickets
    class StatusChoices(models.TextChoices):
        OPEN = 'open', 'Open'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'
        CLOSED = 'closed', 'Closed'
    
    # Priority choices for tickets
    class PriorityChoices(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        CRITICAL = 'critical', 'Critical'
    
    # Ticket title - brief summary of the issue
    title = models.CharField(max_length=200)
    
    # Detailed description of the problem
    description = models.TextField()
    
    # Current status of the ticket
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.OPEN,
    )
    
    # Priority level of the ticket
    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
    )
    
    # Name of the person who created the ticket
    requester_name = models.CharField(max_length=100)
    
    # Email address of the requester
    requester_email = models.EmailField()
    
    # Timestamp when ticket was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Timestamp when ticket was last updated
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']  # Newest tickets first
        verbose_name = 'Support Ticket'
        verbose_name_plural = 'Support Tickets'
    
    def __str__(self):
        """Return a string representation of the ticket."""
        return f"{self.title} ({self.status})"
