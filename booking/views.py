from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions

from booking.models import Booking
from booking.serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows doctors to reserve a room.
    """
    queryset = Booking.objects.all().order_by('-created_at')
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
