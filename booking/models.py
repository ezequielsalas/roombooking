from django.db import models
from django.db.models import Q

from datetime import datetime, date
from datetime import timedelta


class Booking(models.Model):
    room = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    reservation_start = models.DateTimeField(null=True)
    reservation_end = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    expire_at = models.DateTimeField(null=True)

    @classmethod
    def book(cls, room_id, **kwargs):
        expire_at = kwargs.get('expire_at', None)
        start = kwargs.get('start', None)
        end = kwargs.get('end', None)

        if not Booking.is_available(room_id):
            return False
        if expire_at and isinstance(expire_at, int):
            current_time = datetime.now()
            future_time = current_time + timedelta(minutes=expire_at)
            Booking.objects.create(room=room_id, expire_at=future_time)
            return True
        if start and end:
            if not Booking.is_available(room_id, start=start, end=end):
                return False
            Booking.objects.create(room=room_id, reservation_start=start, reservation_end=end)
            return True

        Booking.objects.create(room=room_id)

        return True

    @classmethod
    def delete(cls, booking_id):
        reservation = Booking.objects.get(pk=booking_id, deleted_at__isnull=True)
        reservation.deleted_at = datetime.now()
        reservation.save()

    @classmethod
    def is_available(cls, room_id, start=None, end=None):
        reservation = Booking.objects.filter(room=room_id, deleted_at__isnull=True)
        exists = reservation.exists()
        if not exists:
            return True

        start_range = date.today()
        end_range = date.today()
        if start and end:
            start_range = start
            end_range = end
        scheduled = reservation.exclude(Q(reservation_end__lte=start_range) |
                                        Q(reservation_start__gte=end_range))

        return not scheduled.exists()

    @classmethod
    def release_expired(cls):
        reservations = Booking.objects.filter(expire_at__lte=datetime.now(), deleted_at__isnull=True)
        reservations_qty = reservations.count()
        reservations.update(deleted_at=datetime.now())
        return reservations_qty

    def __str__(self):
        return f"Room: {self.room}"

    class Meta:
        constraints = [models.UniqueConstraint(fields=['created_at', 'room'], condition=Q(deleted_at__isnull=True),
                                               name='unique_booking_per_time')]
