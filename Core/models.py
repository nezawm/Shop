from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# Create your models here.


class OTP(models.Model):
    phone_number = models.CharField(max_length=11, verbose_name=_('Phone Number'))
    code=models.CharField(max_length=6, verbose_name=_('Code'))
    is_verified = models.BooleanField(default=False, verbose_name=_('Is Verified'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    expire_at=models.DateTimeField(verbose_name=_('Expire At'))

    def is_expired(self):
        return timezone.now() > self.expire_at

    def __str__(self):
        return f'OTP is sent for {self.phone_number} successfully, code is---> {self.code}'
