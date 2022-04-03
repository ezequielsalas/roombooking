from django.db import models
from django.db.models import Q


class Booking(models.Model):
    room = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)

    @classmethod
    def book(cls, room_id):
        booking = Booking.objects.filter(room=room_id, deleted_at__isnull=True)
        if booking.exists():
            return False
        Booking.objects.create(room=room_id)
        return True

    def __str__(self):
        return f"Room: {self.room}"

    class Meta:
        constraints = [models.UniqueConstraint(fields=['created_at','room'], condition=Q(deleted_at__isnull=True),
                                              name='unique_booking_per_time')]
