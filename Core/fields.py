import jdatetime
from rest_framework import serializers


class JalaliDateTimeField(serializers.DateTimeField):

    def to_representation(self, value):

        if value is None:
            return None

        return jdatetime.datetime.fromgregorian(
            datetime=value
        ).strftime("%Y/%m/%d %H:%M")