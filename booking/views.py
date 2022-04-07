from celery_once import AlreadyQueued

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from booking.models import Booking
from booking.serializers import BookingSerializer
from booking.tasks import reserve_room


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows doctors to reserve a room.
    """
    queryset = Booking.objects.filter(deleted_at__isnull=True).order_by('-created_at')
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        expire = request.data.get('expire', None)
        serializer = BookingSerializer(data=request.data, many=False, partial=True)
        serializer.is_valid(raise_exception=True)

        booking_requested = serializer.validated_data
        try:
            reserve_room.delay(booking_requested.get('room'), expire_at=expire)
        except AlreadyQueued:
            return Response({"error": "This room is not available"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': "Your request was received"}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        if not pk:
            return Response({"error": "The room id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Booking.delete(pk)
        except Booking.DoesNotExist:
            return Response({"error": "The room id does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': "You reservation was removed"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def verify(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        booking_requested = serializer.validated_data

        if Booking.is_available(booking_requested.get('room')):
            return Response({'message': f"The room {booking_requested.get('room')} is available"},
                            status=status.HTTP_200_OK)

        return Response({'message': "Sorry, the room is not available"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def schedule_booking(self, request, *args, **kwargs):
        room = request.data.get("room")
        schedule_start = request.data.get("reservation_start")
        schedule_end = request.data.get("reservation_end")

        if not room or not schedule_start or not schedule_end:
            return Response({"error": "room, start and End are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reserve_room.delay(room, start=schedule_start, end=schedule_end)
        except AlreadyQueued:
            return Response({"error": "This room is not available"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': "Your request was received"}, status=status.HTTP_200_OK)
