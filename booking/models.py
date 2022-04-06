from django.db import models
from django.db.models import Q

from datetime import datetime
from datetime import timedelta


class Booking(models.Model):
    room = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    expire_at = models.DateTimeField(null=True)

    @classmethod
    def book(cls, room_id, expire_at=None):
        booking = Booking.objects.filter(room=room_id, deleted_at__isnull=True)
        if booking.exists():
            return False
        if expire_at and isinstance(expire_at, int):
            current_time = datetime.now()
            future_time = current_time + timedelta(minutes=expire_at)
            Booking.objects.create(room=room_id, expire_at=future_time)
        Booking.objects.create(room=room_id)
        return True

    @classmethod
    def delete(cls, booking_id):
        reservation = Booking.objects.get(pk=booking_id, deleted_at__isnull=True)
        reservation.deleted_at = datetime.now()
        reservation.save()

    @classmethod
    def search_by_room(cls, room_id):
        reservation = Booking.objects.filter(room=room_id, deleted_at__isnull=True)
        return reservation

    @classmethod
    def release_expired(cls):
        reservations = Booking.objects.filter(expire_at__lte=datetime.now(), deleted_at__isnull=True).update(
            deleted_at=datetime.now())

        return reservations

    def __str__(self):
        return f"Room: {self.room}"

    class Meta:
        constraints = [models.UniqueConstraint(fields=['created_at', 'room'], condition=Q(deleted_at__isnull=True),
                                               name='unique_booking_per_time')]
