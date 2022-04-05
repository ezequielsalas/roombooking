from django.db import models
from django.db.models import Q
from datetime import date


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

    @classmethod
    def delete(cls, booking_id):
        reservation = Booking.objects.get(pk=booking_id, deleted_at__isnull=True)
        reservation.deleted_at = date.today()
        reservation.save()

    @classmethod
    def search_by_room(cls, room_id):
        reservation = Booking.objects.filter(room=room_id, deleted_at__isnull=True)
        return reservation


    def __str__(self):
        return f"Room: {self.room}"

    class Meta:
        constraints = [models.UniqueConstraint(fields=['created_at', 'room'], condition=Q(deleted_at__isnull=True),
                                               name='unique_booking_per_time')]
