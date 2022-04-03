from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task(name='reserve_room')
def reserve_room(room_id):
    logger.info('Booking...')
    print(f"Booking {room_id}")