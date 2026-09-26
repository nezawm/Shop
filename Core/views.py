from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from Core.serializer import SendOtpSerializer, OTPVerifySerializer

User = get_user_model()


@extend_schema(
    tags=['Authentication'], request=SendOtpSerializer)
class OtpCreateView(APIView):

    def post(self, request):
        serializer = SendOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Authentication'], request=OTPVerifySerializer)
class OtpVerifyView(APIView):

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)


        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data['otp']

        otp.is_verified = True
        otp.save()



        user, created = User.objects.get_or_create(
            phone_number=otp.phone_number,


            defaults={
                'username': otp.phone_number,
            }
        )


        print("USER:", user)
        print("CREATED:", created)


        refresh = RefreshToken.for_user(user)

        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response(
            {
                "access": access_token,
                "refresh": refresh_token,
                "detail": "OTP verified successfully",
                "is_new_user": created,
            },
            status=status.HTTP_200_OK
        )
#
# def home(request):
#     return render(request, 'index.html')