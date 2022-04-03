from celery import shared_task
from celery import Celery
from celery_once import QueueOnce
from celery.utils.log import get_task_logger
from rest_framework.exceptions import ValidationError

from booking.models import Booking
from booking_core.celery import app


logger = get_task_logger(__name__)


@app.task(base=QueueOnce)
def reserve_room(room_id):
    logger.info('Booking...')

    if not Booking.book(room_id):
        logger.info(f"Room {room_id} is not available")
        # TODO: Notify the user because the asynchronous behavior
        return

    logger.info(f"Room {room_id} booked successfully")


