from celery_once import AlreadyQueued
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

        try:
            reserve_room.delay(booking_requested.get('room'))
        except AlreadyQueued:
            return Response({"error": "This room is not available"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': "Your request was received"}, status=status.HTTP_200_OK)
