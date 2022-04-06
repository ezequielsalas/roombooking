from rest_framework import serializers
import datetime, time
from booking.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    # expire_at = serializers.IntegerField()

    # def to_representation(self, instance):
    #     output = super(serializers.ModelSerializer, self).to_representation(instance)
    #     if instance.expire_at:
    #         seconds = time.mktime(instance.expire_at.timetuple())
    #         output['expire_at'] = seconds * 60 # to minutes
    #     return output
    #
    # def to_internal_value(self, data):
    #     expire_val = data.get('expire_at')
    #     output = super(serializers.ModelSerializer, self).to_internal_value(data)
    #     if expire_val:
    #         current_time = datetime.now()
    #         future_time = current_time + datetime.timedelta(minutes=expire_val)
    #         output['expire_at'] = future_time
    #     return output

    class Meta:
        model = Booking
        # fields = ('pk','room')
        fields = ('__all__')
        # extra_kwargs = {'expire_at': {'write_only': True}}
