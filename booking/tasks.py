from celery import shared_task
from celery import Celery
from celery_once import QueueOnce
from celery.utils.log import get_task_logger

from booking.models import Booking
from booking_core.celery import app


logger = get_task_logger(__name__)


@app.task(base=QueueOnce)
def reserve_room(room_id):
    logger.info('Booking...')
    booking = Booking.objects.filter(room=room_id, deleted_at__isnull=True)
    if booking.exists():
        print(f"Room {room_id} is not available")
        logger.info(f"Room {room_id} is not available")
        # TODO: Notify the user with websocket
    Booking.objects.create(room=room_id)
    logger.info(f"Room {room_id} booked successfully")

