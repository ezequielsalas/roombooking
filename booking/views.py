from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from booking.models import Booking
from booking.serializers import BookingSerializer
from booking.tasks import reserve_room

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows doctors to reserve a room.
    """
    queryset = Booking.objects.all().order_by('-created_at')
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        booking_requested = serializer.validated_data
        print(f"El booking{booking_requested.get('room')}")
        reserve_room.delay(booking_requested.get('room'))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
