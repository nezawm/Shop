from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.base_models import SoftDeleteModel


# Create your models here.



class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),
    )
    first_name=models.CharField(max_length=30,verbose_name=_('First Name'),null=True,blank=True)
    last_name =models.CharField(max_length=30,verbose_name=_('Last Name'),null=True,blank=True)
    gender=models.CharField(max_length=1,choices=GENDER_CHOICES,verbose_name=_('Gender'),null=True,blank=True)
    phone_number = models.CharField(max_length=11,verbose_name=_('Phone Number'),null=True,blank=True)
    birth_date = models.DateField(verbose_name=_('Birth Date'),null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True,verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    def __str__(self):
        return  f'{self.first_name}-{self.last_name} ({self.phone_number})'

class Address(SoftDeleteModel):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='addresses')
    city=models.CharField(max_length=30,verbose_name=_('City'),null=True,blank=True)
    street=models.CharField(max_length=30,verbose_name=_('Street'),null=True,blank=True)
    postal_code=models.CharField(max_length=10,verbose_name=_('Postal Code'))



    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return f'{self.city}-{self.street}'

class Profile(SoftDeleteModel):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile')
    avatar=models.ImageField(upload_to='profiles',blank=True,null=True)
    phone_number = models.CharField(max_length=11,verbose_name=_('Phone Number'),null=True,blank=True)
    is_verified=models.BooleanField(default=False,verbose_name=_('Is Verified'),null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True,verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return f'{self.user.first_name}-{self.user.last_name} ({self.user.phone_number})'

