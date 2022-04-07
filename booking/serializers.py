from rest_framework import serializers
from booking.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('pk', 'room', 'reservation_start', 'reservation_end', 'reservation_start')
