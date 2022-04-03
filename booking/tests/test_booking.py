import base64

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from booking.models import Booking


class BookingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        user_name = 'testing_login@avaros.ca'
        password = 'Admin123'

        test_user = User.objects.create_user(username=user_name,
                                             email=user_name,
                                             password=password)

        self.user = test_user
        credentials = base64.b64encode(bytes(f'{user_name}:{password}', 'utf8')).decode('utf8')
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + str(credentials)

    def test_booking_room(self):
        test_room = 1
        created = Booking.book(test_room)
        self.assertTrue(created)

    def test_booking_room_occupied(self):
        test_room = 1

        created = Booking.book(test_room)
        not_created = Booking.book(test_room)
        bookings = Booking.objects.filter(room=test_room, deleted_at__isnull=True)

        self.assertEqual(bookings.count(), 1)
        self.assertTrue(created)
        self.assertTrue(not not_created)
