from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return{
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        '--------------------------------------'
        'detail' : 'OTP created successfully'

    }
import jdatetime


def to_jalali(date):
    if not date:
        return None

    return jdatetime.datetime.fromgregorian(
        datetime=date
    ).strftime('%Y/%m/%d %H:%M')