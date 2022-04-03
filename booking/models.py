from django.db import models
from django.db.models import Q


class Booking(models.Model):
    room = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['created_at'], condition=Q(deleted_at__isnull=False),
                                              name='unique_booking_per_time')]
