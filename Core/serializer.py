
import random
from datetime import timedelta

from Core.base_serializer import BaseSerializer
from Core.utils import to_jalali
from django.utils import timezone
from rest_framework import serializers
from Core.models import OTP
class SendOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)

    def validate_phone_number(self, value):


        if not value.startswith('09'):
            raise serializers.ValidationError(
                'Phone number is invalid.'
            )

        if len(value) != 11:
            raise serializers.ValidationError(
                'Phone number must be 11 digits.'
            )

        return value

    def create(self, validated_data):
        phone_number = validated_data['phone_number']

        OTP.objects.filter(
            phone_number=phone_number,
            is_verified=False
        ).delete()

        code = str(random.randint(100000, 999999))

        expire_at = timezone.now() + timedelta(minutes=1)

        otp = OTP.objects.create(
            phone_number=phone_number,
            code=code,
            expire_at=expire_at,
        )

        print(
            f'OTP created for {phone_number} and code is --> {code}'
        )

        return otp


class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):

        otp = OTP.objects.filter(
            phone_number=attrs['phone_number'],
            code=attrs['code'],
            is_verified=False
        ).order_by('-id').first()

        if otp is None:
            raise serializers.ValidationError({
                'code': 'OTP code is invalid'
            })

        if otp.is_expired():
            raise serializers.ValidationError({
                'code': 'OTP has expired'
            })

        attrs['otp'] = otp

        return attrs


